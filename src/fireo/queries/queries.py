import inspect

from fireo.database import db
from fireo.queries import query_result


class QuerySet:
    """Provide operations related to firestore

    Methods
    -------
    create(**kwargs):
        Create new document in firestore collection
    """
    def __init__(self, model):
        self.model = model

    def create(self, **kwargs):
        """Create new document in firestore collection

        Parameters
        ---------
        **kwargs:
            field name and value

        Returns
        -------
        Model instance:
            modified instance or new instance if no mutable instance provided
        """
        return InsertQuery(self.model, **kwargs).exec()


class BaseQuery:
    """Create connection with firestore and provide ref for model collection

    Methods
    -------
    get_ref():
        Provide firestore ref for model collection
    """
    def __init__(self, model_cls):
        self.model_cls = model_cls

    def get_ref(self):
        """Provide firestore ref for model collection"""
        ref = db.conn.collection(self.model_cls.collection_name)
        return ref


class InsertQuery(BaseQuery):
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
        return query_result.ModelFromDict.convert(self.model, self._raw_exec())
