import sys
from rawtxdecode_py.decode import (
    decode_raw_transaction_unsigned,
)


def main():
    raw_tx = sys.argv[1]

    if not raw_tx:
        print("Usage: main.py <raw-transaction-hash>")
        sys.exit(1)

    decode_raw_transaction_unsigned(raw_tx)


if __name__ == "__main__":
    main()
