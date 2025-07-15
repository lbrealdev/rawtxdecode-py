import sys
from rawtxdecode_py.fields import extract_transaction_fields, InnerTransactionFields
from rawtxdecode_py.decode import decode_raw_transaction
from rawtxdecode_py.pubkey import recover_umcompressed_public_key
from rawtxdecode_py.tx import format_tx_output
import json


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

    tx_output = format_tx_output(decode_tx, public_key)
    json_format = json.dumps(tx_output, indent=2)
    print(json_format)


if __name__ == "__main__":
    main()
