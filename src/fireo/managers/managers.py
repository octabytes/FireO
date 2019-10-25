from fireo.fields import NestedModel
from fireo.fields.errors import FieldNotFound
from fireo.queries import query_set as queries


class ManagerError(Exception):
    pass


class ManagerDescriptor:
    """Restrict user to get `Manager` from model instance and from abstract model"""
    def __init__(self, manager):
        self.manager = manager

    def __get__(self, instance, owner):
        if instance is not None:
            raise ManagerError(f'Manager "{self.manager.name}" can not accessible via {owner.__name__} instance')
        if owner._meta.abstract:
            raise ManagerError(f'Manager "{self.manager.name}" is not accessible via {owner.__name__} abstract model')
        return self.manager


class Manager:
    """Manager are used to perform firestore action directly from model class without instance

    Default manager can be accessible via `collection` from model class

    Examples
    -------
    .. code-block:: python
        class User(Model):
            name = TextField()

        user = User.collection.create(name="Azeem")

    Attributes
    ----------
    queryset:
        Read only property, provide operations related to firestore

    parent_key:
        Parent key if any

    name:
        Name of the manager

    model_cls:
        Model where this manger is contributing

    Methods
    -------
    contribute_to_model(model_cls, name="collection"):
        Attach manager to model class

    create(mutable_instance, kwargs): Model instance
        create new document in firestore collection

    update(mutable_instance, kwargs): Model instance
        Update existing document in firestore collection

    get(key): Model instance
        Get document from firestore

    parent(key):
        Parent key if any

    filter(): Model instance
        Get filter document from firestore

    fetch(limit) : generator
        Fetch document from firestore, limit is optional here

    order(field_name):
        Order document by field_name

    delete(key)
        Delete document from firestore, key is optional
    """
    def __init__(self):
        self.model_cls = None
        self.name = None
        self.parent_key = None

    def contribute_to_model(self, model_cls, name="collection"):
        """Attach manager to model class

        This method attach manager to model class

        Parameters
        ----------
        model_cls : Model
            In which model this manager will be attached

        name : str
            What is the name of this manager when it is attaching with model and
            later can be accessible with this name
        """
        self.name = name
        self.model_cls = model_cls
        setattr(model_cls, name, ManagerDescriptor(self))

    @property
    def queryset(self):
        """provide operations related to firestore"""
        return queries.QuerySet(self.model_cls)

    def create(self, mutable_instance=None, **kwargs,):
        """create new document in firestore collection

        Parameters
        ---------
        mutable_instance: Model instance
            Make changes in existing model instance After performing firestore action modified this instance
            adding things init like id, key etc
        """
        field_list = {}
        # if mutable instance is none this mean user is creating document directly from manager
        # For example User.collection.create(name="Azeem") in this case mutable instance will be None
        # If document is creating by directly using manager then check if there is any NestedModel
        # If there is any nested model then get get value from nested model
        if mutable_instance is None:
            for k, v in kwargs.items():
                try:
                    # if this is an id field then save it in field list and pass it
                    f = self.model_cls._meta.get_field(k)
                except FieldNotFound:
                    field_list[k] = v
                    continue
                if isinstance(f, NestedModel):
                    model_instance = v
                    if f.valid_model(model_instance):
                        field_list[f.name] = model_instance._get_fields()
                else:
                    field_list[k] = v
        else:
            field_list = kwargs

        return self.queryset.create(mutable_instance, **field_list)

    def update(self, mutable_instance=None, **kwargs):
        """Update existing document in firestore collection

        Parameters
        ---------
        mutable_instance: Model instance
            Make changes in existing model instance After performing firestore action modified this instance
            adding things init like id, key etc
        """
        return self.queryset.update(mutable_instance, **kwargs)

    def get(self, key):
        """Get document from firestore"""
        return self.queryset.get(key)

    def parent(self, key):
        """Parent collection"""
        self.parent_key = key
        return self

    def filter(self, *args):
        """Get filter document from firestore"""
        return self.queryset.filter(self.parent_key, *args)

    def fetch(self, limit=None):
        """Fetch document from collection"""
        return self.queryset.filter(self.parent_key).fetch(limit)

    def order(self, field_name):
        """Order the document by field name"""
        return self.queryset.filter(self.parent_key).order(field_name)

    def limit(self, number):
        """Limit the document"""
        return self.queryset.filter(self.parent_key).limit(number)

    def delete(self, key=None):
        """Delete document from firestore"""
        if key:
            self.queryset.delete(key)
        else:
            self.queryset.filter(self.parent_key).delete()