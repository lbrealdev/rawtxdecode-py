from eth.vm.forks.arrow_glacier.transactions import (
    ArrowGlacierTransactionBuilder as TransactionBuilder,
)
from eth_utils import to_bytes, keccak, to_hex
from rawtxdecode_py.tx import TransactionType
from rlp.sedes import big_endian_int, Binary, CountableList, List
import rlp
from dataclasses import dataclass
from typing import Tuple, List as TypeList
from hexbytes import HexBytes


@dataclass
class EIP1559UnsignedTransaction:
    chain_id: int
    nonce: int
    max_priority_fee_per_gas: int
    max_fee_per_gas: int
    gas_limit: int
    to: bytes
    value: int
    data: bytes
    access_list: TypeList[Tuple[bytes, TypeList[int]]]


@dataclass
class EIP1559SignedTransaction(EIP1559UnsignedTransaction):
    v: int
    r: int
    s: int


# EIP-1559 unsigned 9 fields
eip1559_unsigned_fields = [
    big_endian_int,  # chain_id
    big_endian_int,  # nonce
    big_endian_int,  # max_priority_fee_per_gas
    big_endian_int,  # max_fee_per_gas
    big_endian_int,  # gas_limit
    Binary.fixed_length(20, allow_empty=True),  # to
    big_endian_int,  # value
    Binary(),  # data
    CountableList(
        List([Binary.fixed_length(20), CountableList(big_endian_int)])
    ),  # access list
]

# EIP-1559 unsigned 12 fields
eip1559_signed_fields = eip1559_unsigned_fields + [
    big_endian_int,  # v (y_parity)
    big_endian_int,  # r
    big_endian_int,  # s
]


class DecodedTransactionWrapper:
    def __init__(self, decoded_tx):
        self._obj = decoded_tx
        self.fields = decoded_tx.__dict__

    def __getattr__(self, attr):
        return getattr(self._obj, attr)


def convert_hex_to_bytes(tx_hex: str) -> bytes:
    """
    :param tx_hex: Hex-encoded Ethereum transaction string (with or without '0x' prefix).
    :return: Transaction as raw bytes.
    """
    return to_bytes(hexstr=tx_hex)


def decode_raw_transaction(tx: str) -> DecodedTransactionWrapper:
    """
    :param tx: Raw Ethereum transaction in bytes format.
    :return: DecodedTransactionWrapper object providing
             both attribute-style access (e.g., .to, .sender)
             and dictionary-style access to transaction fields.
    """
    tx_bytes = convert_hex_to_bytes(tx)
    decoded_tx = TransactionBuilder().decode(tx_bytes)
    return DecodedTransactionWrapper(decoded_tx)


# Function to convert rlp transaction decoded to dictionary
def convert_rlp_to_dict(tx_tuple: tuple) -> dict:
    unsigned_keys = [
        "chain_id",
        "nonce",
        "max_priority_fee_per_gas",
        "max_fee_per_gas",
        "gas_limit",
        "to",
        "value",
        "data",
        "access_list",
    ]

    return dict(zip(unsigned_keys, tx_tuple))


# Function to generate hash from signed/unsigned transaction
def generate_tx_hash(tx_type: int, tx_encoded: bytes) -> str:
    """
    Generate the hash for both signed and unsigned transactions.
    :param tx_type: 0x01 or 0x02
    :param tx_payload: RLP encoded transaction fields
    :return Keccak256 hash as string.
    """
    tx_hash = keccak(HexBytes(tx_type) + tx_encoded)
    return to_hex(tx_hash)


def decode_raw_transaction_unsigned(tx: str):
    """
    Function to decode unsigned transaction (test)
    :param tx: Raw Ethereum transaction in bytes format.
    :return: DecodedTransactionWrapper object providing
             both attribute-style access (e.g., .to, .sender)
             and dictionary-style access to transaction fields.
    """
    tx_bytes = convert_hex_to_bytes(tx)

    # Check if typed transaction
    if tx_bytes[0] in (0x01, 0x02):
        tx_type = tx_bytes[0]
        tx_payload = tx_bytes[1:]
        tx_rlp = rlp.decode(tx_payload)

        # Debug (test)
        try:
            print(f"Transaction type: {TransactionType.from_type_id(tx_type)}")
        except ValueError:
            raise ValueError(f"Transaction type {tx_type:#x} not supported")

        if len(tx_rlp) == 9:
            print("Unsigned transaction!")
            print("Decoding...")

            decode_unsigned_tx = rlp.decode(tx_payload, List(eip1559_unsigned_fields))
            encode_unsigned_tx = rlp.encode(
                decode_unsigned_tx, List(eip1559_unsigned_fields)
            )
            unsigned_tx_hash = generate_tx_hash(tx_type, encode_unsigned_tx)

            print(f"Hash (unsigned): {unsigned_tx_hash}")

            # tx_function = convert_rlp_to_dict(decode_unsigned_tx)
            # # print(tx_function["to"])

            # tx_type_class = EIP1559UnsignedTransaction(*decode_unsigned_tx)
            # # print(tx_type_class)
        else:
            print("Signed transaction!")
            print("Decoding...")

            decode_signed_tx = rlp.decode(tx_payload, List(eip1559_signed_fields))
            encode_signed_tx = rlp.encode(decode_signed_tx, List(eip1559_signed_fields))
            signed_tx_hash = generate_tx_hash(tx_type, encode_signed_tx)

            print(f"Hash (signed): {signed_tx_hash}")
            # print(decode_signed_tx)
            # print(type(decode_signed_tx))
    else:
        tx_legacy = {
            "error": "UNSUPPORTED_TX_TYPE",
            "reason": "Legacy transactions (type 0) are not supported yet."
        }
        print(tx_legacy)
