from typing import TYPE_CHECKING

from fireo.queries import query_wrapper
from fireo.queries.base_query import BaseQuery
from fireo.utils import utils

if TYPE_CHECKING:
    from fireo.models import Model


class RefreshQuery(BaseQuery):
    """Refresh model from firestore

    Refresh model from firestore using Managers

    Examples
    --------
    .. code-block:: python
        class User(Mode):
            name = TextField()
            age = NumberField()

        u = User(name="Azeem", age=26)
        u.save()

        User(age=27).update(u.key)
        u.refresh()

        # Getting model
        user = User.collection.get(u.key)
        print(user.name)  # Azeem
        print(user.age)  # 27

    Methods
    -------
    _raw_exec():
        private method to get documents from firestore

    exec():
        Get document from firestore and wrap them into model
    """

    def __init__(self, model_class, mutable_model: 'Model'):
        super().__init__(model_class)
        super().set_collection_path(key=mutable_model.key)
        self.model = mutable_model
        self.id = utils.get_id(mutable_model.key)

    def _raw_exec(self, transaction=None):
        """Get firestore reference and then get document based on id"""
        ref = self.get_ref().document(self.id)
        return ref.get(transaction=transaction)

    def exec(self, transaction=None):
        """Wrap the query result into model instance"""
        return query_wrapper.ModelWrapper.from_query_result(self.model, self._raw_exec(transaction))
