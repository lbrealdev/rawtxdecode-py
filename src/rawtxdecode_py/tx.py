from rawtxdecode_py.abi import decode_contract_input_data
from typing import Any, Dict
from enum import Enum


class TransactionType(Enum):
    LEGACY_TX = 0
    ACCESS_LIST_TX = 1
    DYNAMIC_FEE_TX = 2

    @classmethod
    def from_type_id(cls, type_id: int) -> str:
        return {
            cls.LEGACY_TX.value: "Legacy",
            cls.ACCESS_LIST_TX.value: "Access List",
            cls.DYNAMIC_FEE_TX.value: "EIP-1559",
        }.get(type_id, "Unknown type")


def format_tx_output(decoded_tx: Any, *args) -> Dict[str, Any]:
    tx_type_id = TransactionType.from_type_id(decoded_tx.type_id)
    tx_to_address = "0x" + decoded_tx.to.hex()
    tx_input_data = decoded_tx.data

    tx_details = {
        "chainId": decoded_tx.chain_id,
        "type": tx_type_id,
        "valid": decoded_tx.is_signature_valid,
        "hash": "0x" + decoded_tx.hash.hex(),
        "nonce": decoded_tx.nonce,
        "gasLimit": decoded_tx.gas,
        "maxFeePerGas": decoded_tx.max_fee_per_gas,
        "maxPriorityFeePerGas": decoded_tx.max_priority_fee_per_gas,
        "from": "0x" + decoded_tx.sender.hex(),
        "to": tx_to_address,
        "publicKey": args[0]["publicKey"],
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
