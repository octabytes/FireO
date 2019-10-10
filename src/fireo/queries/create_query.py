import inspect

from fireo.queries import query_result
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
    def __init__(self, model, **kwargs):
        super().__init__(model)
        self.query = kwargs
        self.model = model
        # If this is called from manager or mutable model is
        # not provided then this `model` will be a class not instance
        # then create new instance from this model class
        if inspect.isclass(model):
            self.model = model()

            # Suppose user is defined the id for model
            # let name id **id**
            id_field = 'id'

            # Check user provide any custom name for id
            if model._meta.id is not None:
                id_field, _ = model._meta.id

            # _id setter in model check either user defined
            # any id or not in model
            setattr(self.model, '_id', kwargs.get(id_field))

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
        return query_result.ModelFromResult.convert(self.model, self._raw_exec())
