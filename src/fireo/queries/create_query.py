from fireo.queries import query_wrapper
from fireo.queries.base_query import BaseQuery


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
    def __init__(self, model_cls, mutable_instance=None, **kwargs):
        super().__init__(model_cls)
        self.query = kwargs
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
        # Attach key to this model for updating this model
        # Purpose of attaching this key is user can update
        # this model after getting it
        #
        # For example:
        #   u = User.collection.create(name="Azeem", age=25)
        #   u.name = "Updated Name"
        #   u.update()
        self.model.update_doc = self.model.key

        # Reset the field list and changed list
        # This is important to reset so we can
        # find next time which fields are changed
        # when we are going to update it
        self.model.field_list = []
        self.model.field_changed = []

    def _doc_ref(self):
        """create document ref from firestore"""
        return self.get_ref().document(self.model._id)

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
        return {
            f.db_column_name: f.get_value(self.query.get(f.name))
            for f in self.model._meta.field_list.values()
        }

    def _raw_exec(self):
        """save model into firestore and return the document"""
        ref = self._doc_ref()
        ref.set(self._parse_field())
        return ref.get()

    def exec(self):
        """return modified or new instance of model"""
        return query_wrapper.ModelWrapper.from_query_result(self.model, self._raw_exec())
