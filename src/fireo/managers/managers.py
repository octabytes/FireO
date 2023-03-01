import base64
import json

from fireo.queries.query_set import QuerySet


class ManagerError(Exception):
    pass


class ManagerDescriptor:
    """Restrict user to get `Manager` from model instance and from abstract model"""

    def __init__(self, manager):
        self.manager = manager

    def __get__(self, instance, owner):
        # reset parent key
        self.manager._parent_key = None
        if instance is not None:
            raise ManagerError(
                f'Manager "{self.manager.name}" can not accessible via {owner.__name__} instance')
        if owner._meta.abstract:
            raise ManagerError(
                f'Manager "{self.manager.name}" is not accessible via {owner.__name__} abstract model')
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

    _parent_key:
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

    _update(mutable_instance, kwargs): Model instance
        Update existing document in firestore collection

    get(key): Model instance
        Get document from firestore

    get_all(key_list): Model instance
        Get All documents according to key list

    parent(key):
        Parent key if any

    filter(): Model instance
        Get filter document from firestore

    fetch(limit) : generator
        Fetch document from firestore, limit is optional here

    group_fetch(limit) : generator
        Use a collection group query to retrieve documents from a collection group

    transaction():
        Firestore transaction

    batch():
        Firestore batch writes

    limit(count):
        Set limit for query

    offset(num_to_skip)
        Set offset for query

    order(field_name):
        Order document by field_name

    delete(key, child=False)
        Delete document from firestore, key is optional

    delete_all(key_list, batch=None, child=False)
        Delete all documents according to given keys

    cursor(c):
        Start query from specific point

    start_after(key, **kwargs):
        Start document after this key or after that matching fields

    start_at(key, **kwargs):
        Start document at this key or at that matching fields

    end_before(key, **kwargs):
        End document after this key or before that matching fields

    end_at(key, **kwargs):
        End document at this key or at that matching fields
    """

    def __init__(self):
        self.model_cls = None
        self.name = None
        self._parent_key = None

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
        return QuerySet(self.model_cls)

    def create(self, mutable_instance=None, transaction=None, batch=None, merge=None, no_return=False, **kwargs):
        """create new document in firestore collection

        Parameters
        ---------
        mutable_instance: Model instance
            Make changes in existing model instance After performing firestore action modified this instance
            adding things init like id, key etc

        transaction:
            Firestore transaction

        batch:
            Firestore batch
        """
        if self._parent_key:
            kwargs['parent'] = self._parent_key

        return self.queryset.create(mutable_instance, transaction, batch, merge, no_return, **kwargs)

    def _update(self, mutable_instance, transaction=None, batch=None):
        """Update existing document in firestore collection

        Parameters
        ---------
        mutable_instance: Model instance
            Make changes in existing model instance After performing firestore action modified this instance
            adding things init like id, key etc

        transaction:
            Firestore transaction

        batch:
            Firestore batch
        """
        return self.queryset.update(mutable_instance, transaction, batch)

    def get(self, key, transaction=None):
        """Get document from firestore"""
        return self.queryset.get(key, transaction)

    def get_all(self, key_list):
        """Get All documents according to key list"""
        for key in key_list:
            yield self.queryset.get(key)

    def _refresh(self, mutable_instance, transaction=None):
        """Refresh document from firestore"""
        return self.queryset.refresh(mutable_instance, transaction)

    def parent(self, key):
        """Parent collection"""
        self._parent_key = key
        return self

    def filter(self, *args, **kwargs):
        """Get filter document from firestore"""
        return self.queryset.filter(self._parent_key, *args, **kwargs)

    def fetch(self, limit=None):
        """Fetch document from collection"""
        return self.queryset.filter(self._parent_key).fetch(limit)

    def group_fetch(self, limit=None):
        """A collection group consists of all collections with the same ID.
        By default, queries retrieve results from a single collection in your database.
        Use a collection group query to retrieve documents from a collection group
        instead of from a single collection."""
        return self.queryset.filter(self._parent_key).group_fetch(limit)

    def transaction(self, t):
        """Firestore transaction"""
        return self.queryset.filter(self._parent_key).transaction(t)

    def batch(self, b):
        """Firestore batch"""
        return self.queryset.filter(self._parent_key).batch(b)

    def limit(self, count):
        """Limit the document"""
        return self.queryset.filter(self._parent_key).limit(count)

    def offset(self, num_to_skip):
        """Set offset for query"""
        return self.queryset.filter(self._parent_key).offset(num_to_skip)

    def order(self, field_name):
        """Order the document by field name"""
        return self.queryset.filter(self._parent_key).order(field_name)

    def delete(self, key=None, transaction=None, batch=None, child=False):
        """Delete document from firestore

        if child is True then delete child collection and documents also
        """
        if key:
            self.queryset.delete(key, transaction, batch, child=child)
        else:
            self.queryset.filter(self._parent_key).delete(child=child)

    def delete_all(self, key_list, batch=None, child=False):
        """Delete all documents according to given keys"""
        for key in key_list:
            self.queryset.delete(key, batch=batch, child=child)

    def cursor(self, cursor):
        """Start query from specific point

        Cursor define where to start the query
        """
        parent = self._parent_key
        cursor_dict = json.loads(base64.b64decode(cursor))
        if 'parent' in cursor_dict:
            parent = cursor_dict['parent']
        query = self.queryset.filter(parent)
        if 'filters' in cursor_dict:
            for filter in cursor_dict['filters']:
                query.filter(*filter)
        if 'order' in cursor_dict:
            query.order(cursor_dict['order'])
        if 'limit' in cursor_dict:
            query.limit(cursor_dict['limit'])

        # check if last doc key is available or not
        if 'last_doc_key' in cursor_dict:
            query.start_after(key=cursor_dict['last_doc_key'])
        else:
            query.offset(cursor_dict['offset'])

        return query

    def start_after(self, key=None, **kwargs):
        """Start document after this key or after that matching fields"""
        return self.queryset.filter(self._parent_key).start_after(key, **kwargs)

    def start_at(self, key=None, **kwargs):
        """Start document at this key or at that matching fields"""
        return self.queryset.filter(self._parent_key).start_at(key, **kwargs)

    def end_before(self, key=None, **kwargs):
        """End document after this key or after that matching fields"""
        return self.queryset.filter(self._parent_key).end_before(key, **kwargs)

    def end_at(self, key=None, **kwargs):
        """End document at this key or at that matching fields"""
        return self.queryset.filter(self._parent_key).end_at(key, **kwargs)
