import sys
from rawtxdecode_py.fields import extract_transaction_fields, InnerTransactionFields
from rawtxdecode_py.decode import decode_raw_transaction
from rawtxdecode_py.pubkey import recover_umcompressed_public_key
from rawtxdecode_py.abi import decode_contract_input_data
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


def decoded_tx_output(decoded_tx: Any, public_key: str) -> Dict[str, Any]:
    tx_type_id = TransactionType.from_type_id(decoded_tx.type_id)
    tx_to_address = "0x" + decoded_tx.to.hex()
    tx_input_data = decoded_tx.data

    tx_details = {
        "chainId": str(decoded_tx.chain_id),
        "type": str(tx_type_id),
        "valid": decoded_tx.is_signature_valid,
        "hash": "0x" + decoded_tx.hash.hex(),
        "nonce": str(decoded_tx.nonce),
        "gasLimit": str(decoded_tx.gas),
        "maxFeePerGas": str(decoded_tx.max_fee_per_gas),
        "maxPriorityFeePerGas": str(decoded_tx.max_priority_fee_per_gas),
        "from": "0x" + decoded_tx.sender.hex(),
        "to": tx_to_address,
        "publicKey": public_key["publicKey"],
        "v": f"{decoded_tx.y_parity:02x}",
        "r": format(decoded_tx.r, "064x"),
        "s": format(decoded_tx.s, "064x"),
        "value": str(decoded_tx.value),
    }

    if len(tx_input_data) != 0:
        input_data = "0x" + tx_input_data.hex()
        contract_function = decode_contract_input_data(tx_to_address, input_data)

        tx_details.update(
            {
                "input": input_data,
                "functionHash": "0x" + decoded_tx.data[:4].hex(),
                "functionName": contract_function["functionName"],
                "decodedInputs": contract_function["decodedInputs"],
            }
        )

    return tx_details


def _stringify_json(data):
    if isinstance(data, dict):
        return {k: _stringify_json(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [_stringify_json(v) for v in data]
    elif isinstance(data, bool):
        return data
    elif isinstance(data, bytes):
        return "0x" + data.hex()
    else:
        return str(data)


def main():
    raw_tx_hex = sys.argv[1:]

    if not raw_tx_hex:
        print("Usage: decode <raw-transaction-hash>")
        sys.exit(1)

    decode_tx = decode_raw_transaction(raw_tx_hex[0])

    tx_type = decode_tx.type_id
    tx_data = decode_tx.data
    tx_fields = InnerTransactionFields(decode_tx._inner)

    # Ordered and formatted transaction dictionary
    ordered_fields = extract_transaction_fields(tx_fields, tx_type, tx_data)

    # Extract v, r, s components from decoded transaction
    v, r, s = decode_tx.y_parity, decode_tx.r, decode_tx.s

    public_key = recover_umcompressed_public_key(ordered_fields, v, r, s)

    tx_output = decoded_tx_output(decode_tx, public_key)

    # json output `default`
    # json_format = json.dumps(tx_output, indent=2)
    # print(json_format)

    # json output `stringify`
    stringify_json = _stringify_json(tx_output)
    json_format = json.dumps(stringify_json, indent=2)
    print(json_format)


if __name__ == "__main__":
    main()
