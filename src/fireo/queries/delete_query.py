from fireo.queries.base_query import BaseQuery


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

    def __init__(self, model_cls, id):
        super().__init__(model_cls)
        self.id = id

    def _delete_collection(self):
        ref = self.get_ref().document(self.id).delete()
        return ref

    def exec(self):
        return self._delete_collection()
