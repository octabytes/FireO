from fireo.queries.base_query import BaseQuery
from fireo.utils import utils
from fireo.database import db


class DeleteQuery(BaseQuery):
    """Delete Document from firestore

    Example
    ------
    .. code-block:: python
        class User(Mode):
            name = TextField()
            age = NumberField()

        u = User(name="Azeem", age=26)
        u.save()

        # Deleting model
        id = User.collection.delete(u.id)
        print(id)

    Methods
    -------
    _delete_collection():
        private method for executing operation in firestore for deleting documents

    exec(transaction_or_batch):
        execute the delete operation
    """

    def __init__(self, model_cls, key=None, query=None, child=False):
        super().__init__(model_cls)
        self.child = child
        self.transaction_or_batch = None
        self.query = query
        self.id = utils.get_id(key)
        if key:
            super().set_collection_path(key=key)

    def _delete_document(self):
        ref = self.get_ref().document(self.id)

        if self.child:
            for c in ref.collections():
                DeleteQuery(self.model_cls, query=c, child=True).exec(self.transaction_or_batch)

        if self.transaction_or_batch is not None:
            self.transaction_or_batch.delete(ref)
        else:
            ref.delete()
        return self.id

    def _delete_collection(self, batch_size=100):
        docs = self.query.limit(batch_size).get()
        deleted = 0

        for doc in docs:
            ref = doc.reference

            if self.child:
                for c in ref.collections():
                    DeleteQuery(self.model_cls, query=c, child=True).exec(self.transaction_or_batch)

            if self.transaction_or_batch is not None:
                self.transaction_or_batch.delete(ref)
            else:
                ref.delete()
            deleted = deleted + 1

        if deleted >= batch_size:
            return self._delete_collection(batch_size)

    def exec(self, transaction_or_batch=None):
        self.transaction_or_batch = transaction_or_batch
        if self.id:
            self._delete_document()
        else:
            self._delete_collection()
