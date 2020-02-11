from fireo.fields import NestedModel
from fireo.queries import query_wrapper
from fireo.queries.base_query import BaseQuery
from fireo.utils import utils


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
    def __init__(self, model_cls, mutable_instance=None, **kwargs):
        super().__init__(model_cls)
        self.query = kwargs
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
        field_dict = {}
        for f in self.model._meta.field_list.values():
            # Check if it is nested model
            if isinstance(f, NestedModel):
                # Get nested model field
                self._nested_field_list(f, field_dict, f.name)
            else:
                v = f.get_value(self.query.get(f.name), ignore_required=True)
                if v or type(v) is bool:
                    field_dict[f.db_column_name] = v
        return field_dict

    def _nested_field_list(self, f, fl, *name):
        """Get Nested Fields"""
        nested_field_list = {}
        for n_f in f.nested_model._meta.field_list.values():
            if isinstance(n_f, NestedModel):
                n = (*name, n_f.name)
                self._nested_field_list(n_f, nested_field_list, *n)
            else:
                nested_field_list[n_f.db_column_name] = n_f.get_value(
                    utils.get_nested(self.query, *name).get(n_f.name),
                    ignore_required=True
                )
        fl[f.db_column_name] = nested_field_list

    def _raw_exec(self, transaction_or_batch=None):
        """Update document in firestore and return the document"""
        ref = self._doc_ref()
        if transaction_or_batch:
            transaction_or_batch.update(ref, self._parse_field())
            return None
        ref.update(self._parse_field())
        return ref.get()

    def exec(self, transaction_or_batch=None):
        """return modified instance of model"""
        if transaction_or_batch:
            return self._raw_exec(transaction_or_batch)
        return query_wrapper.ModelWrapper.from_query_result(self.model, self._raw_exec())
