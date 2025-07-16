import sys
from rawtxdecode_py.decode import decode_raw_transaction


def main():
    raw_tx_hex = sys.argv[1]

    if not raw_tx_hex:
        print("Usage: main.py <raw-transaction-hash>")
        sys.exit(1)

    decode_raw_tx = decode_raw_transaction(raw_tx_hex)
    tx_fields = decode_raw_tx.fields["_inner"].as_dict()

    # print(dir(decode_raw_tx))

    # Debug transaction fields
    for key, value in tx_fields.items():
        print(f"key: {key} - value: {value}")


if __name__ == "__main__":
    main()
