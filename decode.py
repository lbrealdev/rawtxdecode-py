from eth.vm.forks.arrow_glacier.transactions import (
    ArrowGlacierTransactionBuilder as TransactionBuilder,
)
from eth_utils import to_bytes


class DecodedTransactionWrapper:
    def __init__(self, decoded_tx):
        self._obj = decoded_tx
        self.fields = decoded_tx.__dict__

    def __getattr__(self, attr):
        return getattr(self._obj, attr)


def convert_hex_to_bytes(tx_hex: str) -> bytes:
    """
    :param tx_hex: Hex-encoded Ethereum transaction string (with or without '0x' prefix).
    :return: Transaction as raw bytes.
    """
    return to_bytes(hexstr=tx_hex)


def decode_raw_transaction(tx: str) -> DecodedTransactionWrapper:
    """
    :param tx: Raw Ethereum transaction in bytes format.
    :return: DecodedTransactionWrapper object providing
             both attribute-style access (e.g., .to, .sender)
             and dictionary-style access to transaction fields.
    """
    tx_bytes = convert_hex_to_bytes(tx)
    decoded_tx = TransactionBuilder().decode(tx_bytes)
    return DecodedTransactionWrapper(decoded_tx)
