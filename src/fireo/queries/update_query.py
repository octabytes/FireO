from fireo.queries import query_wrapper
from fireo.queries.base_query import BaseQuery
from fireo.utils import utils
from fireo.utils.types import DumpOptions
from fireo.utils.utils import get_flat_dict


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

    def __init__(self, model_cls, mutable_instance):
        super().__init__(model_cls)
        self.model = mutable_instance
        super().set_collection_path(key=mutable_instance.key)

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
        self.model._id = ref.id  #
        if transaction_or_batch is not None:
            transaction_or_batch.update(ref, self._parse_field())
            return ref

        parse_field = self._parse_field()
        if parse_field:
            ref.update(parse_field)
            return ref.get()

    def exec(self, transaction_or_batch=None):
        """return modified instance of model"""
        if transaction_or_batch is not None:
            return self._raw_exec(transaction_or_batch)
        return query_wrapper.ModelWrapper.from_query_result(self.model, self._raw_exec())
