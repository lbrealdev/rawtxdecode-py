from hexbytes import HexBytes


def extract_trasaction_fields(decoded):
    """
    clojure function
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

    # Convert dictionary fields to HexBytes
    def converted_fields():
        for k, v in ordered_tx_fields.items():
            if isinstance(v, bytes):
                ordered_tx_fields[k] = HexBytes(v)
        return ordered_tx_fields

    return converted_fields
