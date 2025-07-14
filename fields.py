from typing import Any, Dict
from hexbytes import HexBytes


def extract_transaction_fields(decoded: Any) -> Dict[str, Any]:
    """
    :param decoded: Decoded transaction object containing transaction fields.
    :return: Ordered and formatted transaction dictionary for unsigned transaction serialization.
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

    for k, v in ordered_tx_fields.items():
        if isinstance(v, bytes):
            ordered_tx_fields[k] = HexBytes(v)

    return ordered_tx_fields
