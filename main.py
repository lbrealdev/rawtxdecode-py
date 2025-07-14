from eth_utils import decode_hex
from eth_keys.datatypes import Signature
from eth_account._utils.signing import extract_chain_id, to_standard_v
from eth_account._utils.legacy_transactions import (
    serializable_unsigned_transaction_from_dict,
)
import sys

from fields import (
    extract_transaction_fields,
    InnerTransactionFields,
)
from decode import decode_raw_transaction


def get_tx_signature(v: int, r: int, s: int) -> Signature:
    """
    :param v: Recovery identifier from Ethereum transaction signature.
    :param r: R component of the ECDSA signature.
    :param s: S component of the ECDSA signature.
    :return: Signature object in VRS (standardized) format.
    """
    signature = Signature(vrs=(to_standard_v(extract_chain_id(v)[1]), r, s))
    return signature


def get_unsigned_tx_hash(tx_dict) -> tuple[str, bytes]:
    """
    :param tx_dict: Dictionary with unsigned Ethereum transaction fields.
    :return: Tuple with the transaction hash as (hex string, raw bytes).
    """
    tx = serializable_unsigned_transaction_from_dict(tx_dict)
    tx_hash_bytes = tx.hash()
    return tx_hash_bytes.hex(), tx_hash_bytes


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

    # Create signature object
    signature = get_tx_signature(v, r, s)

    # Hash of the unsigned transaction (to verify signature)
    unsigned_hash = get_unsigned_tx_hash(ordered_fields)
    tx_hash_bytes = decode_hex(unsigned_hash[0])

    # Recover the public key from the signature and transaction hash
    public_key = signature.recover_public_key_from_msg_hash(tx_hash_bytes)

    # Convert public key to uncompressed SEC1 format (0x04 + X + Y)
    uncompressed_public_key = b"\x04" + public_key.to_bytes()
    uncompressed_public_key_hex = "0x" + uncompressed_public_key.hex()

    print(uncompressed_public_key_hex)


if __name__ == "__main__":
    main()
