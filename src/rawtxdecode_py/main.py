import sys
from rawtxdecode_py.fields import extract_transaction_fields, InnerTransactionFields
from rawtxdecode_py.decode import decode_raw_transaction
from rawtxdecode_py.pubkey import recover_umcompressed_public_key
from typing import Any, Dict
import json
from enum import Enum


class TransactionType(Enum):
    LEGACY = 0
    ACCESS_LIST = 1
    EIP1559 = 2

    @classmethod
    def from_type_id(cls, type_id: int) -> str:
        return {
            cls.LEGACY.value: "Legacy",
            cls.ACCESS_LIST.value: "Access List",
            cls.EIP1559.value: "EIP-1559",
        }.get(type_id, "Unknown type")


def decoded_tx_output(decoded_tx: Any, *args) -> Dict[str, Any]:
    tx_type_id = TransactionType.from_type_id(decoded_tx.type_id)
    tx_input_data = decoded_tx.data

    tx_data = {
        "chainId": decoded_tx.chain_id,
        "type": tx_type_id,
        "valid": decoded_tx.is_signature_valid,
        "hash": "0x" + decoded_tx.hash.hex(),
        "nonce": decoded_tx.nonce,
        "gasLimit": decoded_tx.gas,
        "maxFeePerGas": decoded_tx.max_fee_per_gas,
        "maxPriorityFeePerGas": decoded_tx.max_priority_fee_per_gas,
        "from": "0x" + decoded_tx.sender.hex(),
        "to": "0x" + decoded_tx.to.hex(),
        "publicKey": args[0]["publicKey"],
        "v": f"{decoded_tx.y_parity:02x}",
        "r": format(decoded_tx.r, "064x"),
        "s": format(decoded_tx.s, "064x"),
        "value": str(decoded_tx.value),
    }

    if len(tx_input_data) != 0:
        tx_data.update(
            {
                "input": "0x" + decoded_tx.data.hex(),
                "functionHash": "0x" + decoded_tx.data[:4].hex(),
                "possibleFunctions": "tbd",
            }
        )

    return tx_data


def main():
    raw_tx_hex = sys.argv[1:]

    if not raw_tx_hex:
        print("Usage: decode <raw-transaction-hash>")
        sys.exit(1)

    decode_tx = decode_raw_transaction(raw_tx_hex[0])

    # Ordered and formatted transaction dictionary
    tx_type = decode_tx.type_id
    tx_data = decode_tx.data
    tx_fields = InnerTransactionFields(decode_tx._inner)

    ordered_fields = extract_transaction_fields(tx_fields, tx_type, tx_data)

    # Extract v, r, s components from decoded transaction
    v, r, s = decode_tx.y_parity, decode_tx.r, decode_tx.s

    public_key = recover_umcompressed_public_key(ordered_fields, v, r, s)

    tx_output = decoded_tx_output(decode_tx, public_key)
    json_format = json.dumps(tx_output, indent=2)
    print(json_format)


if __name__ == "__main__":
    main()
