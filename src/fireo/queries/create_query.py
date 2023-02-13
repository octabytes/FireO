from fireo.managers.errors import EmptyDocument
from fireo.queries import query_wrapper
from fireo.queries.base_query import BaseQuery
from fireo.utils.types import DumpOptions


class CreateQuery(BaseQuery):
    """Insert model into firestore

    Methods
    ------
    _doc_ref():
        create document ref from firestore

    _parse_field():
        Get and return `db_value` from model `_meta`

    _raw_exec():
        save model into firestore and return the document

    exec():
        return modified or new instance of model
    """

    def __init__(self, model_cls, mutable_instance=None, no_return=False, **kwargs):
        super().__init__(model_cls)
        self.no_return = no_return
        # If this is called from manager or mutable model is
        # not provided then this `model` will be a class not instance
        # then create new instance from this model class
        # otherwise set mutable instance to self.model
        if mutable_instance:
            self.model = mutable_instance
            super().set_collection_path(key=mutable_instance.key)
        else:
            self.model = model_cls()

            # Suppose user is defined the id for model
            # let name id **id**
            id_field = 'id'

            # Check user provide any custom name for id
            if model_cls._meta.id is not None:
                id_field, _ = model_cls._meta.id

            # _id setter in model check either user defined
            # any id or not in model
            setattr(self.model, '_id', kwargs.get(id_field))
            # Check if there is any parent
            parent = kwargs.get('parent')
            if parent:
                self.model.parent = parent
                super().set_collection_path(path=parent)

        for k, v in kwargs.items():
            setattr(self.model, k, v)

        # Attach key to this model for updating this model
        # Purpose of attaching this key is user can update
        # this model after getting it
        #
        # For example:
        #   u = User.collection.create(name="Azeem", age=25)
        #   u.name = "Updated Name"
        #   u.update()
        self.model._update_doc = self.model.key

    def _doc_ref(self):
        """create document ref from firestore"""
        return self.get_ref().document(self.model._id)

    def _parse_field(self, ignore_unchanged=False):
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
        field_list = self.model.to_db_dict(dump_options=DumpOptions(
            ignore_default_none=self.model._meta.ignore_none_field,
            ignore_unchanged=ignore_unchanged,
        ))

        if not field_list:
            raise EmptyDocument(
                "Empty document can not be save, Add at least one field value"
            )

        return field_list

    def _raw_exec(self, transaction_or_batch=None, merge=None):
        """save model into firestore and return the document"""
        ref = self._doc_ref()
        if transaction_or_batch is not None:
            if merge:
                transaction_or_batch.set(
                    ref, self._parse_field(), merge=merge)
            else:
                transaction_or_batch.set(ref, self._parse_field())
            return ref

        if merge:
            ref.set(self._parse_field(ignore_unchanged=True), merge=merge)
        else:
            ref.set(self._parse_field())

        # Reset the field changed list
        # This is important to reset, so we can
        # find next time which fields are changed
        # when we are going to update it
        self.model._field_changed = []

        # If no_return is True then return nothing otherwise 
        # return object instance issue #126
        if self.no_return:
            return None
        else:
            return ref.get()

    def exec(self, transaction_or_batch=None, merge=None):
        """return modified or new instance of model"""
        if transaction_or_batch is not None:
            return self._raw_exec(transaction_or_batch, merge)
        return query_wrapper.ModelWrapper.from_query_result(self.model, self._raw_exec(merge=merge))
