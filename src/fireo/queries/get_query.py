from fireo.queries import query_result
from fireo.queries.base_query import BaseQuery


class GetQuery(BaseQuery):
    """Get model from firestore

    Get model from firestore using Managers

    Examples
    --------
    .. code-block:: python
        class User(Mode):
            name = TextField()
            age = NumberField()

        u = User(name="Azeem", age=26)
        u.save()

        # Getting model
        user = User.collection.get(u.id)
        print(user.name)  # Azeem
        print(user.age)  # 26

    Methods
    -------
    _raw_exec():
        private method to get documents from firestore

    exec():
        Get document from firestore and wrap them into model
    """

    def __init__(self, model_cls, id):
        super().__init__(model_cls)
        self.model = model_cls()
        self.id = id

    def _raw_exec(self):
        """Get firestore reference and then get document based on id"""
        ref = self.get_ref().document(self.id)
        return ref.get()

    def exec(self):
        """Wrap the query result into model instance"""
        return query_result.ModelFromResult.convert(self.model, self._raw_exec())