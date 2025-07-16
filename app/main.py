from rawtxdecode_py.decode import decode_raw_transaction
from rawtxdecode_py.fields import extract_transaction_fields, InnerTransactionFields
from rawtxdecode_py.pubkey import recover_umcompressed_public_key
from rawtxdecode_py.tx import format_tx_output


def lambda_handler(event, context):
    raw_tx_hex = event.get("hex")

    if not raw_tx_hex:
        return {"error": "hex is required."}

    decode_raw_tx = decode_raw_transaction(raw_tx_hex)

    tx_type = decode_raw_tx.type_id
    tx_data = decode_raw_tx.data
    tx_fields = InnerTransactionFields(decode_raw_tx._inner)

    tx_fields_ordered = extract_transaction_fields(tx_fields, tx_type, tx_data)

    v, r, s = decode_raw_tx.y_parity, decode_raw_tx.r, decode_raw_tx.s

    public_key = recover_umcompressed_public_key(tx_fields_ordered, v, r, s)

    raw_tx_output = format_tx_output(decode_raw_tx, public_key)

    return raw_tx_output
