from fireo.queries import query_wrapper
from fireo.queries.base_query import BaseQuery
from fireo.utils import utils


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
        user = User.collection.get(u.key)
        print(user.name)  # Azeem
        print(user.age)  # 26

    Methods
    -------
    _raw_exec():
        private method to get documents from firestore

    exec():
        Get document from firestore and wrap them into model
    """

    def __init__(self, model_cls, key):
        super().__init__(model_cls)
        super().set_collection_path(key=key)
        self.model = model_cls()
        # set parent to this model if any
        self.model.parent = utils.get_parent_doc(key)
        # Attach key to this model for updating this model
        # Purpose of attaching this key is user can update
        # this model after getting it
        #
        # For example:
        #   u = User.collection.get(user_key)
        #   u.name = "Updated Name"
        #   u.update()
        self.model._update_doc = key
        self.id = utils.get_id(key)

    def _raw_exec(self, transaction=None):
        """Get firestore reference and then get document based on id"""
        ref = self.get_ref().document(self.id)
        return ref.get(transaction=transaction)

    def exec(self, transaction=None):
        """Wrap the query result into model instance"""
        return query_wrapper.ModelWrapper.from_query_result(self.model, self._raw_exec(transaction))
