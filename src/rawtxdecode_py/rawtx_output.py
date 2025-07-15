from typing import Any, Dict
from enum import Enum
from rawtxdecode_py.abi import decode_contract_input_data


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


def create_tx_output(decoded_tx: Any, public_key: str) -> Dict[str, Any]:
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


def stringify_json(data):
    """
    :param data: Any Python object (dict, list, or value) to stringify.
    :return: Same structure with all values converted to strings, except booleans.
    """
    if isinstance(data, dict):
        return {k: stringify_json(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [stringify_json(v) for v in data]
    elif isinstance(data, bool):
        return data
    elif isinstance(data, bytes):
        return "0x" + data.hex()
    else:
        return str(data)
