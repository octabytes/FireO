from fireo.fields import NestedModel
from fireo.queries import query_wrapper
from fireo.queries.base_query import BaseQuery


class UpdateQuery(BaseQuery):
    """Update document in firestore

    Methods
    ------
    _doc_ref():
        create document ref from firestore

    _parse_field():
        Get and return `db_value` from model `_meta`

    _raw_exec():
        Update document in firestore and return the document

    exec():
        return modified instance of model
    """
    def __init__(self, model_cls, mutable_instance=None, **kwargs):
        super().__init__(model_cls)
        self.query = kwargs
        self.model = mutable_instance
        super().set_collection_path(key=mutable_instance.key)

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
        field_dict = {}
        for f in self.model._meta.field_list.values():
            # Check if it is nested model
            if isinstance(f, NestedModel):
                # Get nested model field
                for nested_f in f.nested_model._meta.field_list.values():
                    v = nested_f.get_value(self.query.get(f.name+"."+nested_f.name), ignore_required=True)
                    if v:
                        # create the name with parent field name and child name
                        # For example:
                        #   class User(Model):
                        #       address = TextField()
                        #   class Student(Model):
                        #       age = NumberField()
                        #       user = NestedModel(User)
                        #
                        # Then the field name for nested model will be "user.address"
                        field_dict[f.db_column_name+"."+nested_f.db_column_name] = v
            else:
                v = f.get_value(self.query.get(f.name), ignore_required=True)
                if v:
                    field_dict[f.db_column_name] = v
        return field_dict

    def _raw_exec(self):
        """Update document in firestore and return the document"""
        ref = self._doc_ref()
        ref.update(self._parse_field())
        return ref.get()

    def exec(self):
        """return modified instance of model"""
        return query_wrapper.ModelWrapper.from_query_result(self.model, self._raw_exec())
