from typing import Optional, Type, TYPE_CHECKING

from fireo.queries import query_wrapper
from fireo.queries.base_query import BaseQuery
from fireo.utils import utils
from fireo.utils.types import DumpOptions
from fireo.utils.utils import get_flat_dict

if TYPE_CHECKING:
    from fireo.models import Model


class UpdateQuery(BaseQuery):
    """Update document in firestore

    Methods
    ------
    _doc_ref():
        create document ref from firestore

    _parse_field():
        Get and return `db_value` from model `_meta`

    _raw_exec(transaction_or_batch):
        Update document in firestore and return the document

    exec(transaction_or_batch):
        return modified instance of model
    """

    def __init__(
        self,
        model_cls: 'Type[Model]',
        mutable_instance: 'Optional[Model]' = None,
        no_return: bool = False,
        key: Optional[str] = None,
        values: Optional[dict] = None,
    ):
        super().__init__(model_cls)
        assert mutable_instance is None or isinstance(mutable_instance, model_cls), (
            'mutable_instance must be instance of model_cls'
        )
        assert mutable_instance is not None or key is not None, (
            'mutable_instance or key is required'
        )

        self.model = mutable_instance
        if self.model is None:
            self.model = model_cls()

        if key is not None:
            self.model.key = key

        if values is not None:
            self.model.merge_with_dict(values)

        self.no_return = no_return
        super().set_collection_path(key=self.model.key)

    def _doc_ref(self):
        """create document ref from firestore"""
        return self.get_ref().document(utils.get_id(self.model.key))

    def _parse_field(self):
        """Get and return `db_value` from model `_meta`

        Examples
        -------
        .. code-block:: python
            class User(Model):
                name = TextField(column_name="full_name")
                age = NumberField()

            User.collection.create(name="Azeem", age=25)

        This method return dict of field names and values
        in this case it will be like this
        `{full_name: "Azeem", age=25}`
        """
        field_dict = self.model.to_db_dict(dump_options=DumpOptions(
            ignore_required=True,
            ignore_default=True,
            ignore_unchanged=True,
        ))

        # Convert to dot notated fields update objects without replacing
        flat_field_dict = get_flat_dict(field_dict)

        return flat_field_dict

    def _raw_exec(self, transaction_or_batch=None):
        """Update document in firestore and return the document"""
        ref = self._doc_ref()
        self.model._id = ref.id
        values = self._parse_field()

        if transaction_or_batch is not None:
            if values:
                transaction_or_batch.update(ref, values)
            return ref

        if values:
            ref.update(values)

        self.model._reset_field_changed()

        if self.no_return:
            return None

        return ref.get()

    def exec(self, transaction_or_batch=None):
        """return modified instance of model"""
        if transaction_or_batch is not None:
            return self._raw_exec(transaction_or_batch)
        return query_wrapper.ModelWrapper.from_query_result(self.model, self._raw_exec())
