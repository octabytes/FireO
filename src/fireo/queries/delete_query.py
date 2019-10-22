from fireo.queries.base_query import BaseQuery
from fireo.utils import utils


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

    exec():
        execute the delete operation
    """

    def __init__(self, model_cls, key=None, query=None):
        super().__init__(model_cls)
        self.query = query
        self.id = utils.get_id(key)
        if key:
            super().set_collection_path(key=key)

    def _delete_document(self):
        self.get_ref().document(self.id).delete()
        return self.id

    def _delete_collection(self, batch_size=100):
        docs = self.query.limit(batch_size).get()
        deleted = 0

        for doc in docs:
            doc.reference.delete()
            deleted = deleted + 1

        if deleted >= batch_size:
            return self._delete_collection(batch_size)

    def exec(self):
        if self.id:
            self._delete_document()
        else:
            self._delete_collection()
