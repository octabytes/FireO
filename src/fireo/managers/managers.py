from functools import wraps
from typing import Any, Dict, Generic, Iterator, List, Optional, overload, Type, TYPE_CHECKING, TypeVar, Union

from google.cloud.firestore_v1 import DocumentReference, Transaction, WriteBatch

from fireo.queries.query_set import QuerySet
from fireo.utils.cursor import Cursor
from fireo.utils.utils import get_key, is_key

if TYPE_CHECKING:
    from fireo.queries.filter_query import FilterQuery
    from fireo.models import Model

    try:
        from typing import Self
    except ImportError:
        try:
            from typing_extensions import Self
        except ImportError:
            Self = Any


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


def _convert_key_or_id_to_key(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        if 'id' in kwargs:
            kwargs['key'] = self.get_key_by_id(kwargs.pop('id'))
        elif 'key' in kwargs:
            pass
        elif args:
            arg = args[0]
            if not is_key(arg):
                args = (self.get_key_by_id(arg),) + args[1:]

        return func(self, *args, **kwargs)

    return wrapper


def _convert_key_or_id_list_to_keys_list(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        if 'id_list' in kwargs:
            kwargs['key_list'] = [self.get_key_by_id(id_) for id_ in kwargs.pop('id_list')]
        elif 'key_list' in kwargs:
            pass
        elif args:
            key_or_id_list = args[0]
            if key_or_id_list:
                if not is_key(key_or_id_list[0]):
                    args = ([self.get_key_by_id(id_) for id_ in key_or_id_list],) + args[1:]

        return func(self, *args, **kwargs)

    return wrapper


ModelType = TypeVar('ModelType', bound='Model')


class Manager(Generic[ModelType]):
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

    def __init__(self, *, model_cls=None, name=None, parent_key=None):
        self.model_cls = model_cls
        self.name = name
        self._parent_key = parent_key

    def _deconstruct(self) -> Dict[str, Any]:
        return {
            "model_cls": self.model_cls,
            "name": self.name,
            "parent_key": self._parent_key,
        }

    def copy(self, **kwargs) -> "Manager":
        return type(self)(**{**self._deconstruct(), **kwargs})

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
    def queryset(self) -> QuerySet:
        """provide operations related to firestore"""
        return QuerySet(self.model_cls)

    def create(
        self, mutable_instance=None, transaction=None, batch=None, merge=None, no_return=False, **kwargs
    ) -> Optional[ModelType]:
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

    @overload
    def update(
        self,
        key: Optional[str] = None,
        mutable_instance: Optional[ModelType] = None,
        transaction: Optional[Transaction] = None,
        batch: Optional[WriteBatch] = None,
        no_return: bool = False,
        **kwargs
    ) -> Optional[Union[ModelType, DocumentReference]]:
        ...

    @_convert_key_or_id_to_key
    def update(
        self, key=None, mutable_instance=None, transaction=None, batch=None, no_return=False, **kwargs
    ) -> Optional[Union[ModelType, DocumentReference]]:
        """Update existing document in firestore collection

        Parameters
        ---------
        key: str
            Key of the document. If key is not provided then mutable_instance is required

        mutable_instance: Model instance
            Make changes in existing model instance After performing firestore action modified this instance
            adding things init like id, key etc

        transaction:
            Firestore transaction

        batch:
            Firestore batch

        no_return:
            If True, then updated document will not be fetched from firestore

        **kwargs:
            Extra fields to be updated
        """
        assert key or mutable_instance, "Either key or mutable_instance is required"
        assert not key or is_key(key), "Key is not valid"

        return self.queryset.update(key, mutable_instance, transaction, batch, no_return, **kwargs)

    @overload
    def get(self, key: str, transaction: Optional[Transaction] = None) -> Optional[ModelType]:
        ...

    @overload
    def get(self, id: str, transaction: Optional[Transaction] = None) -> Optional[ModelType]:
        ...

    @_convert_key_or_id_to_key
    def get(self, key: str, transaction: Optional[Transaction] = None) -> Optional[ModelType]:
        """Get document from firestore"""
        assert is_key(key), "Key is not valid"

        return self.queryset.get(key, transaction)

    @overload
    def get_all(self, key_list: List[str]) -> Iterator[Optional[ModelType]]:
        ...

    @overload
    def get_all(self, id_list: List[str]) -> Iterator[Optional[ModelType]]:
        ...

    @_convert_key_or_id_list_to_keys_list
    def get_all(self, key_list: List[str]) -> Iterator[Optional[ModelType]]:
        """Get All documents according to key list"""
        for key in key_list:
            yield self.queryset.get(key)

    def refresh(self, mutable_instance: ModelType, transaction=None) -> None:
        """Refresh document from firestore"""
        self.queryset.get(mutable_instance.key, transaction, mutable_instance)

    def parent(self, key: str) -> "Self":
        """Parent collection"""
        return self.copy(parent_key=key)

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

    def transaction(self, t: Transaction):
        """Firestore transaction"""
        return self.queryset.filter(self._parent_key).transaction(t)

    def batch(self, b: WriteBatch):
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

    @overload
    def delete(
        self,
        key: str,
        transaction: Optional[Transaction] = None,
        batch: Optional[WriteBatch] = None,
        child: bool = False
    ) -> None:
        ...

    @overload
    def delete(
        self,
        id: str,
        transaction: Optional[Transaction] = None,
        batch: Optional[WriteBatch] = None,
        child: bool = False
    ) -> None:
        ...

    @_convert_key_or_id_to_key
    def delete(
        self,
        key: str,
        transaction: Optional[Transaction] = None,
        batch: Optional[WriteBatch] = None,
        child: bool = False
    ) -> None:
        """Delete document from firestore

        if child is True then delete child collection and documents also
        """
        self.queryset.delete(key, transaction, batch, child=child)

    @overload
    def delete_all(self, key_list: List[str], batch: Optional[WriteBatch] = None, child: bool = False) -> None:
        ...

    @overload
    def delete_all(self, id_list: List[str], batch: Optional[WriteBatch] = None, child: bool = False) -> None:
        ...

    @_convert_key_or_id_list_to_keys_list
    def delete_all(self, key_list: List[str], batch: Optional[WriteBatch] = None, child: bool = False) -> None:
        """Delete all documents according to given keys"""
        for key in key_list:
            self.queryset.delete(key, batch=batch, child=child)

    def delete_every(self, child: bool = False) -> None:
        """Delete every document from the collection"""
        self.queryset.filter(self._parent_key).delete(child=child)

    def cursor(self, cursor):
        """Start query from specific point

        Cursor define where to start the query
        """
        return Cursor.from_string(cursor).apply(self._parent_key, self.queryset)

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

    def get_key_by_id(self, id: str) -> str:
        """Get document key by id"""
        # return self.queryset.get_key_by_id(id)
        self.model_cls: Type[Model]
        return get_key(self.model_cls.collection_name, id, self._parent_key)
