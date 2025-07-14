from typing import Any, Dict
from hexbytes import HexBytes


class InnerTransactionFields:
    def __init__(self, inner: Any):
        self.__inner = inner

    def as_dict(self) -> Dict[str, Any]:
        return self.__inner.as_dict()


def extract_transaction_fields(
    fields: InnerTransactionFields, type_id: int, data: bytes
) -> Dict[str, Any]:
    """
    :param fields: Dictionary containing core transaction fields.
    :param type_id: Transaction type identifier (e.g., 2 for EIP-1559).
    :param data: Transaction input data in bytes.
    :return: Ordered and formatted dictionary for unsigned transaction serialization.
    """

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

    inner = fields.as_dict()

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

    tx_fields.update({"type": type_id, "data": data})

    ordered_tx_fields = {
        rename_map.get(k, k): (tx_fields[k] if k in tx_fields else None)
        for k in ordered_keys
        if k in tx_fields
    }

    for k, v in ordered_tx_fields.items():
        if isinstance(v, bytes):
            ordered_tx_fields[k] = HexBytes(v)

    return ordered_tx_fields
