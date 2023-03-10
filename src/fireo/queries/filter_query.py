from enum import Enum
from functools import partial

from google.cloud import firestore
from google.cloud.firestore_v1.field_path import FieldPath

from fireo.database import db
from fireo.fields import MapField
from fireo.queries import query_wrapper
from fireo.queries.base_query import BaseQuery
from fireo.queries.delete_query import DeleteQuery
from fireo.queries.query_iterator import QueryIterator
from fireo.utils import utils
from fireo.utils.types import DumpOptions
from fireo.utils.utils import (
    get_dot_names_as_dot_columns,
    get_nested_field_by_dotted_name,
)


class Ordering(str, Enum):
    ASCENDING = "Asc"
    DESCENDING = "Desc"


class FilterQuery(BaseQuery):
    """Filter documents on the bases of where clauses

    Filter document by filed name, You can also sort and limit the documents.

    Attributes
    ----------
    model: Model
        Model instance

    select_query: list
        Where filter

    limit: int
        Number of documents

    order: list
        Order the documents

    query_transaction:
        Firestore transaction

    query_batch:
        Firestore batch writes

    Methods
    -------
    transaction(transaction):
        Set Firestore transaction

    batch(batch):
        Set Firestore transaction

    parse_where():
        parse where filter

    query()
        Make a query that perform operation in firestore

    _fields_by_column_name():
        Change the field name according to their db column name

    _is_id_field(name):
        Check if this is id field

    _firestore_doc():
        Get document from firestore based on key

    start_after(model):
        Start fetching document after the specific model(document)

    start_at(model):
        Start fetching document at the specific model(document)

    end_before(model):
        End fetching document before the specific model(document)

    end_at(model):
        End fetching document at the specific model(document)

    filter(args):
        Apply filter for querying document

    limit(count):
        Apply limit on number of documents

    offset(num_to_skip):
        Define query offset

    order(field_name):
        Order document by field name

    fetch(limit):
        Fetch document from firestore, limit is optional here

    get():
        Get the first matching document from firestore

    delete():
        Delete the filter documents

    _update_doc_key(model):
        Attach key to model for later updating the model
    """

    def __init__(
        self,
        model_cls,
        parent=None,
        *,
        # private use
        select_query=None,
        limit=None,
        offset=None,
        order=None,
        start_after=None,
        start_at=None,
        end_before=None,
        end_at=None,
        query_transaction=None,
        query_batch=None,
        **kwargs,
    ):
        super().__init__(model_cls, **kwargs)
        self.parent = parent
        self._select_query = (select_query or []).copy()
        self._limit = limit
        self._offset = offset
        self._order = (order or []).copy()
        self._start_after = start_after
        self._start_at = start_at
        self._end_before = end_before
        self._end_at = end_at
        self._query_transaction = query_transaction
        self._query_batch = query_batch
        if parent:
            self.set_collection_path(path=parent)

    def _deconstruct(self):
        return {
            **super()._deconstruct(),
            'parent': self.parent,
            'select_query': self._select_query,
            'limit': self._limit,
            'offset': self._offset,
            'order': self._order,
            'start_after': self._start_after,
            'start_at': self._start_at,
            'end_before': self._end_before,
            'end_at': self._end_at,
            'query_transaction': self._query_transaction,
            'query_batch': self._query_batch,
        }

    def transaction(self, t):
        return self.copy(query_transaction=t)

    def batch(self, b):
        return self.copy(query_batch=b)

    def _parse_where(self):
        """Parse where filter

        User can change the field column name in firestore So, filter where clauses
        on the base of db column name
        """
        filters = []
        for w in self._select_query:
            name, op, val = w

            # ISSUE # 160
            # check if it is ID field
            if self._is_id_field(name):
                # should yield "__name__"
                db_col_name = FieldPath.document_id()

                # value should an reference
                if type(val) is list:
                    val = [self._get_ref_by_key_or_id(v) for v in val]
                else:
                    val = self._get_ref_by_key_or_id(val)
            else:
                field = get_nested_field_by_dotted_name(self.model_cls, name)
                db_col_name = get_dot_names_as_dot_columns(self.model_cls, name)

                if not isinstance(field, MapField):
                    serialise_value = partial(
                        field.get_value,
                        dump_options=DumpOptions(ignore_required=True, ignore_default=True)
                    )
                    if op == 'array_contains':
                        val = serialise_value([val])[0]
                    elif op in ('in', 'not_in'):
                        val = [serialise_value(v) for v in val]
                    else:
                        val = serialise_value(val)

            filters.append((db_col_name, op, val))
        return filters

    def _get_ref_by_key_or_id(self, key_or_id):
        """Get document reference by key or id"""
        key = key_or_id
        if not utils.is_key(key_or_id):
            key = self.model_cls.collection_name + "/" + key_or_id
            if self.model_cls.parent:
                key = self.model_cls.parent + "/" + key

        return db.conn.document(key)

    @property
    def query(self):
        """Make a query for firestore"""
        ref = self.get_ref()
        # parse where filter
        for f in self._parse_where():
            ref = ref.where(*f)
        # Apply limit
        if self._limit:
            ref = ref.limit(self._limit)
        # Apply offset
        if self._offset:
            ref = ref.offset(self._offset)
        # order the documents
        for o in self._order:
            name, direction = o
            db_column = get_dot_names_as_dot_columns(self.model_cls, name)
            ref = ref.order_by(db_column, direction=direction)

        if self._start_after:
            ref = ref.start_after(self._start_after)
        if self._start_at:
            ref = ref.start_at(self._start_at)
        if self._end_before:
            ref = ref.end_before(self._end_before)
        if self._end_at:
            ref = ref.end_at(self._end_at)

        return ref

    def _fields_by_column_name(self, **kwargs):
        """Change the field name according to their db column name"""
        return {
            self.model_cls._meta.get_field(k).db_column_name: v
            for k, v in kwargs.items()
        }

    # ISSUE # 160
    def _is_id_field(self, name):
        """Check if this is id field"""
        # should yield "__name__"
        if name == FieldPath.document_id():
            return True

        if name == '_id':
            return True

        # Checking `model._meta.id` because `model._id` or `model.id` are not
        # populated on CLS
        field_name, field = self.model_cls._meta.id
        if name == field_name and not field.include_in_document:
            return True

        return False

    def _firestore_doc(self, key):
        """Get document from firestore based on key"""
        return db.conn.collection(utils.get_parent(key)).document(utils.get_id(key)).get()

    def start_after(self, key=None, **kwargs):
        """Start document after this"""
        assert not key or not kwargs, "Cannot use both key and kwargs"
        if key:
            start_after = self._firestore_doc(key)
        else:
            start_after = self._fields_by_column_name(**kwargs)

        return self.copy(start_after=start_after)

    def start_at(self, key=None, **kwargs):
        """Start document at this point"""
        if key:
            start_at = self._firestore_doc(key)
        else:
            start_at = self._fields_by_column_name(**kwargs)

        return self.copy(start_at=start_at)

    def end_before(self, key=None, **kwargs):
        """End document before this point"""
        if key:
            end_before = self._firestore_doc(key)
        else:
            end_before = self._fields_by_column_name(**kwargs)

        return self.copy(end_before=end_before)

    def end_at(self, key=None, **kwargs):
        """End document at this point"""
        if key:
            end_at = self._firestore_doc(key)
        else:
            end_at = self._fields_by_column_name(**kwargs)

        return self.copy(end_at=end_at)

    def filter(self, *args, **kwargs):
        """Apply filter for querying document

        Apply where filter as many as you want

        Parameters
        ---------
        args: Tuple
            Contain three things 1- field name, 2-operation, 3-value

        kwargs:
            keyword args Direct assign for equal filter

        Returns
        -------
        self:
            Return self object
        """
        select_query = []
        if args:
            select_query.append(args)

        elif kwargs:
            for k, v in kwargs.items():
                select_query.append((k, '==', v))

        return self.copy(select_query=[*self._select_query, *select_query])

    def limit(self, count):
        """Apply limit for query"""
        return self.copy(limit=count)

    def offset(self, num_to_skip):
        """Offset for query"""
        return self.copy(offset=num_to_skip)

    def order(self, field_name):
        """Order document by field name

        By default, a query retrieves all documents that satisfy the query in ascending order by document ID.
        You can specify the sort order for your data using `order()`, and you can limit the number of documents
        retrieved using `limit()`

        Put a dash(-) in front of field name if you want to sort it in descending order. You can also combine
        filter with order

        Parameters
        ----------
        field_name : str
            Name of the field on which base order is applied

        Returns
        -------
            Self object
        """
        order_direction = firestore.Query.ASCENDING
        name = field_name

        # If this is in Desc order
        if field_name[0] == '-':
            order_direction = firestore.Query.DESCENDING
            name = field_name[1:]  # Get the field name after dash(-) e.g -age name will be age

        return self.copy(order=[*self._order, (name, order_direction)])

    def fetch(self, limit=None):
        """Fetch the result from firestore

        Parameters
        ---------
        limit : optional
            Apply limit to firestore documents, how much documents you want to retrieve
        """
        query = self
        if limit:
            query = self.copy(limit=limit)
        return QueryIterator(query)  # todo

    def group_fetch(self, limit=None):
        return self.copy(group_collection=True).fetch(limit)

    def get(self):
        """Get the first matching document from firestore

        Get first matching document and convert it into model and return it
        This is same as `fetch(limit=1)` the only difference is `get()` method
        return **model instance** and the `fetch()` method return the **generator**
        """
        filter_query = self.copy(limit=1)
        doc = next(filter_query.query.stream(filter_query._query_transaction), None)
        if doc:
            m = query_wrapper.ModelWrapper.from_query_result(filter_query.model_cls(), doc)
            return m

        return None

    def delete(self, child=False):
        """Delete the filter documents

        if child is True then delete nested collection and documents also
        """
        transaction_or_batch = self._query_transaction if self._query_transaction else self._query_batch
        DeleteQuery(self.model_cls, query=self.query, child=child).exec(transaction_or_batch)

    def _update_doc_key(self, model):
        """Attach key to model for later updating the model

        Attach key to this model for updating this model
        Purpose of attaching this key is user can update
        this model after getting it

        For example:
          u = User.collection.get(user_key)
          u.name = "Updated Name"
          u.update()

        Parameters
        ----------
        model:
            Current model where update key need to attach

        Returns
        -------
        update_doc_key:
            Doc key for updating document
        """
        if self.parent:
            update_doc_key = self.parent + '/' + model.collection_name + '/' + utils.get_id(model.key)
        else:
            update_doc_key = model.key
        return update_doc_key
