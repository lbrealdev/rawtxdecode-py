from eth.vm.forks.arrow_glacier.transactions import (
    ArrowGlacierTransactionBuilder as TransactionBuilder,
)


class DecodedTransactionWrapper:
    def __init__(self, decoded_tx):
        self._obj = decoded_tx
        self.fields = decoded_tx.__dict__

    def __getattr__(self, attr):
        return getattr(self._obj, attr)


def decode_raw_transaction(tx: bytes) -> DecodedTransactionWrapper:
    """
    :param tx: Raw Ethereum transaction in bytes format.
    :return: DecodedTransactionWrapper object providing
             both attribute-style access (e.g., .to, .sender)
             and dictionary-style access to transaction fields.
    """
    decoded_tx = TransactionBuilder().decode(tx)
    return DecodedTransactionWrapper(decoded_tx)
