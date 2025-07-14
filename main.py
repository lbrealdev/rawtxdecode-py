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
from hexbytes import HexBytes
import sys


def convert_hex_to_bytes(hex_str: str) -> bytes:
    return to_bytes(hexstr=hex_str)


def decode_raw_transaction(tx: bytes) -> dict:
    decoded_tx = TransactionBuilder().decode(tx)
    return decoded_tx


def extract_trasaction_fields(decoded):
    ordered_keys = [
        "to",
        "nonce",
        "value",
        "gas",
        "chain_id",
        "max_fee_per_gas",
        "max_priority_fee_per_gas",
        "type",
        "data",
    ]

    rename_map = {
        "chain_id": "chainId",
        "max_fee_per_gas": "maxFeePerGas",
        "max_priority_fee_per_gas": "maxPriorityFeePerGas",
    }

    inner = decoded.__dict__.get("_inner").as_dict()

    tx_fields = {
        k: inner[k]
        for k in [
            "to",
            "nonce",
            "value",
            "gas",
            "chain_id",
            "max_fee_per_gas",
            "max_priority_fee_per_gas",
        ]
    }

    tx_fields.update({"type": decoded.type_id, "data": decoded.data})

    ordered_tx_fields = {
        rename_map.get(k, k): (tx_fields[k] if k in tx_fields else None)
        for k in ordered_keys
        if k in tx_fields
    }

    return ordered_tx_fields


def main():
    hex_input = sys.argv[1]

    tx_bytes = convert_hex_to_bytes(hex_input)
    decode_tx = decode_raw_transaction(tx_bytes)
    fields = extract_trasaction_fields(decode_tx)

    print(fields)


if __name__ == "__main__":
    main()
