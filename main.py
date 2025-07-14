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

from fields import extract_trasaction_fields


def convert_hex_to_bytes(hex_str: str) -> bytes:
    return to_bytes(hexstr=hex_str)


def decode_raw_transaction(tx: bytes) -> dict:
    decoded_tx = TransactionBuilder().decode(tx)
    return decoded_tx


def main():
    hex_input = sys.argv[1]

    tx_bytes = convert_hex_to_bytes(hex_input)
    decode_tx = decode_raw_transaction(tx_bytes)
    fields = extract_trasaction_fields(decode_tx)

    # print(fields())

    # Convert to and data fields from bytes to HexBytes
    # for k, v in fields.items():
    #     if isinstance(v, bytes):
    #         fields[k] = HexBytes(v)

    # Debug fields dict types
    # for k, v in fields().items():
    #     print(f"Key: {k}, Value: {type(v)}")

    serializable_tx_from_dict = serializable_unsigned_transaction_from_dict(fields())
    encoded_hash = serializable_tx_from_dict.hash().hex()

    print(encoded_hash)


if __name__ == "__main__":
    main()
