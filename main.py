import sys
from fields import (
    extract_transaction_fields,
    InnerTransactionFields,
)
from decode import decode_raw_transaction
from pubkey import recover_umcompressed_public_key


def main():
    raw_tx_hex = sys.argv[1]

    decode_tx = decode_raw_transaction(raw_tx_hex)

    # Ordered and formatted transaction dictionary
    tx_type = decode_tx.type_id
    tx_data = decode_tx.data
    tx_fields = InnerTransactionFields(decode_tx._inner)

    ordered_fields = extract_transaction_fields(tx_fields, tx_type, tx_data)

    # Extract v, r, s components from decoded transaction
    v, r, s = decode_tx.y_parity, decode_tx.r, decode_tx.s

    public_key = recover_umcompressed_public_key(ordered_fields, v, r, s)

    print(public_key)


if __name__ == "__main__":
    main()
