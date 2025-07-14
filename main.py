from eth.vm.forks.arrow_glacier.transactions import (
    ArrowGlacierTransactionBuilder as TransactionBuilder,
)
from eth_utils import (
    to_bytes,
    decode_hex,
)
from eth_keys.datatypes import Signature, PublicKey
from eth_account._utils.signing import extract_chain_id, to_standard_v
from eth_account._utils.legacy_transactions import (
    serializable_unsigned_transaction_from_dict,
)
import sys

from fields import extract_transaction_fields


def convert_hex_to_bytes(tx_hex: str) -> bytes:
    """
    :param tx_hex: Hex-encoded Ethereum transaction string (with or without '0x' prefix).
    :return: Transaction as raw bytes.
    """
    return to_bytes(hexstr=tx_hex)


def decode_raw_transaction(tx: bytes) -> dict:
    decoded_tx = TransactionBuilder().decode(tx)
    return decoded_tx


def tx_signature(v, r, s):
    signature = Signature(vrs=(to_standard_v(extract_chain_id(v)[1]), r, s))
    return signature


def get_unsigned_tx_hash(tx_dict) -> tuple[str, bytes]:
    """
    :param tx_dict: Dictionary with unsigned Ethereum transaction fields.
    :return: Tuple with the transaction hash as (hex string, raw bytes).
    """
    tx = serializable_unsigned_transaction_from_dict(tx_dict)
    tx_hash_bytes = tx.hash()
    return tx_hash_bytes.hex(), tx_hash_bytes


def main():
    hex_input = sys.argv[1]

    tx_bytes = convert_hex_to_bytes(hex_input)
    decode_tx = decode_raw_transaction(tx_bytes)

    fields = extract_transaction_fields(decode_tx)

    vrs = {
        "v": decode_tx.y_parity,
        "r": decode_tx.r,
        "s": decode_tx.s,
    }

    sign = tx_signature(vrs["v"], vrs["r"], vrs["s"])

    # Debug fields dict types
    # for k, v in fields().items():
    #     print(f"Key: {k}, Value: {type(v)}")

    # Debug vrs dict types
    # for k, v in vrs.items():
    #     print(f"Key: {k}, Value: {type(v)}")

    unsigned_tx_object = serializable_unsigned_transaction_from_dict(fields)
    unsigned_tx_hash_bytes = decode_hex(unsigned_tx_object.hash().hex())
    public_key = sign.recover_public_key_from_msg_hash(unsigned_tx_hash_bytes)

    # unsigned_tx_hash_hex = unsigned_tx_object.hash().hex()
    # unsigned_tx_hash_bytes = decode_hex(unsigned_tx_hash_hex)

    # print(f"hex: {unsigned_tx_hash_hex}")
    # print(f"bytes: {unsigned_tx_hash_bytes}")
    # print(f"test: {unsigned_tx_hash_bytes}")

    # print(decode_tx.y_parity)

    test = get_unsigned_tx_hash(fields)
    test_unsigned = decode_hex(test[0])
    test_pubkey = sign.recover_public_key_from_msg_hash(test_unsigned)

    print(sign)
    print(public_key)
    print(test_pubkey)


if __name__ == "__main__":
    main()
