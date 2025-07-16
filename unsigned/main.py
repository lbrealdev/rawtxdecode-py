import sys
from rawtxdecode_py.decode import (
  decode_raw_transaction, 
  decode_unsigned_raw_transaction, 
  decode_raw_transaction_test,
  decode_raw_transaction_typed
)
import json


def main():
    raw_tx_hex = sys.argv[1]

    if not raw_tx_hex:
        print("Usage: main.py <raw-transaction-hash>")
        sys.exit(1)



    # test unsigned transaction #01
    print()
    print("#01 - Default with HexBytes")
    print()

    decode_unsigned_raw_tx_1 = decode_unsigned_raw_transaction(raw_tx_hex)
    # print(dir(decode_unsigned_raw_tx_1))

    # Debug transaction fields #01
    tx_fields_1 = decode_unsigned_raw_tx_1.fields["_inner"].as_dict()
    for key, value in tx_fields_1.items():
        print(f"key: {key} - value: {value}")
    


    # test unsigned transaction #02
    print()
    print("#02 - Default")
    print()

    decode_unsigned_raw_tx_2 = decode_raw_transaction_test(raw_tx_hex)
    # print(dir(decode_unsigned_raw_tx_2))

    tx_fields_2 = decode_unsigned_raw_tx_2.fields["_inner"].as_dict()
    for key, value in tx_fields_2.items():
        print(f"key: {key} - value: {value}")

    

    # test unsigned transaction #03
    print()
    print("#03 - TypedTransaction (unsigned/signed)")
    print()
    
    decode_unsigned_raw_tx_3 = decode_raw_transaction_typed(raw_tx_hex)
    # print(dir(decode_unsigned_raw_tx_3))
    
    # TypedTransaction don't has _inner
    tx_fields_3 = decode_unsigned_raw_tx_3.fields["transaction"].as_dict()
    for key, value in tx_fields_3.items():
        print(f"key: {key} - value: {value}")




    # tx_fields = decode_raw_tx.

    # decode_raw_tx = decode_raw_transaction(raw_tx_hex)
    # tx_fields = decode_raw_tx.fields["_inner"].as_dict()

    # print(dir(decode_raw_tx))


if __name__ == "__main__":
    main()
