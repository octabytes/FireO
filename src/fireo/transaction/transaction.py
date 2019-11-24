from google.cloud import firestore

from fireo.database import db


class Transaction:
    """Provide a callable object to use as a transactional decorater."""

    def __init__(self, to_wrap):
        self.to_wrap = to_wrap

    def __call__(self, transaction, *args, **kwargs):
        @firestore.transactional
        def operate_transaction(transaction, *args, **kwargs):
            return self.to_wrap(transaction, *args, **kwargs)

        return operate_transaction(transaction, *args, **kwargs)