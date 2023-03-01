from datetime import datetime

from google.cloud import firestore
from google.cloud.firestore_v1.field_path import FieldPath

from fireo.database import db
from fireo.fields import DateTime, ReferenceField
from fireo.fields.errors import FieldNotFound
from fireo.queries import query_wrapper
from fireo.queries.base_query import BaseQuery
from fireo.queries.delete_query import DeleteQuery
from fireo.queries.query_iterator import QueryIterator
from fireo.utils import utils
from fireo.utils.utils import get_db_column_names_for_path


class FilterQuery(BaseQuery):
    """Filter documents on the bases of where clauses

    Filter document by filed name, You can also sort and limit the documents.

    Attributes
    ----------
    model: Model
        Model instance

    select_query: list
        Where filter

    n_limit: int
        Number of documents

    oderer_by: list
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

    def __init__(self, model_cls, parent=None, *args, **kwargs):
        super().__init__(model_cls)
        self.model = model_cls()
        self.select_query = self._where_filter(*args, **kwargs)
        self.n_limit = None
        self._offset = None
        self.order_by = []
        self.parent = parent
        self.cursor_dict = {}
        self._start_after = None
        self._start_at = None
        self._end_before = None
        self._end_at = None
        self.query_transaction = None
        self.query_batch = None
        if parent:
            super().set_collection_path(path=parent)
            # Add parent in cursor
            self.cursor_dict['parent'] = parent

    def _where_filter(self, *args, **kwargs):
        """For Direct assign of filter when equality operator"""
        if args:
            return [args]
        elif kwargs:
            filter = []
            for k, v in kwargs.items():
                filter.append((k, '==', v))
            return filter
        else:
            return []

    def transaction(self, t):
        self.query_transaction = t
        return self

    def batch(self, b):
        self.query_batch = b
        return self

    def parse_where(self):
        """Parse where filter

        User can change the field column name in firestore So, filter where clauses
        on the base of db column name
        """
        filters = []
        for w in self.select_query:
            name, op, val = w

            # save the filter in cursor for next fetch
            #
            # ISSUE # 77
            # if filter value type is datetime then it need to first
            # convert into string then JSON serialize
            cf = w
            if type(val) is datetime:
                cf = (name, op, val.isoformat())

            if 'filters' in self.cursor_dict:
                self.cursor_dict['filters'].append(cf)
            else:
                self.cursor_dict['filters'] = [cf]

            try:
                # ISSUE # 77
                # if field is datetime and type is str (which is usually come from cursor)
                # then convert this string into datetime format
                if isinstance(self.model._meta.get_field(name), DateTime) and type(val) is str:
                    val = datetime.fromisoformat(val)

                # ISSUE # 78
                # check if field is ReferenceField then to query this field we have to
                # convert this value into document reference then filter it
                if isinstance(self.model._meta.get_field(name), ReferenceField):
                    # ISSUE # 116
                    # ReferenceFields can be optional and None
                    # in which case, do not update val to a doc that doesn't exist
                    if val is not None:
                        val = db.conn.document(val)
            except FieldNotFound:
                # Filter with nested model not able to find the field (e.g user.name)
                # it require to loop the nested model first to find the field
                # so just ignore it
                pass

            # check if user defined to set the value as lower case
            if self.model._meta.to_lowercase and type(val) is str:
                val = val.lower()

            # ISSUE # 160
            # check if it is ID field
            if self._is_id_field(name):
                # should yield "__name__"
                f_name = FieldPath.document_id()

                # value should be an array
                if type(val) is list:
                    val = [self._get_ref_by_key_or_id(v) for v in val]
                else:
                    val = self._get_ref_by_key_or_id(val)
            else:
                f_name = self._get_db_column_name(name)
            filters.append((f_name, op, val))
        return filters

    def _get_ref_by_key_or_id(self, key_or_id):
        """Get document reference by key or id"""
        key = key_or_id
        if not utils.is_key(key_or_id):
            key = self.model.collection_name + "/" + key_or_id
            if self.model.parent:
                key = self.model.parent + "/" + key

        return db.conn.document(key)

    def _get_db_column_name(self, name):
        model = self.model
        db_field_path = get_db_column_names_for_path(model, *name.split('.'))

        f_name = '.'.join(db_field_path)
        return f_name

    def query(self):
        """Make a query for firestore"""
        ref = self.get_ref()
        # parse where filter
        for f in self.parse_where():
            ref = ref.where(*f)
        # Apply limit
        if self.n_limit:
            ref = ref.limit(self.n_limit)
        # Apply offset
        if self._offset:
            ref = ref.offset(self._offset)
        # order the documents
        for o in self.order_by:
            name, direction = o
            if direction == 'Desc':
                ref = ref.order_by(name, direction=firestore.Query.DESCENDING)
            else:
                ref = ref.order_by(name)

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
            self.model._meta.get_field(k).db_column_name: v
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
        field_name, field = self.model._meta.id
        if name == field_name and not field.include_in_document:
            return True

        return False

    def _firestore_doc(self, key):
        """Get document from firestore based on key"""
        return db.conn.collection(utils.get_parent(key)).document(utils.get_id(key)).get()

    def start_after(self, key=None, **kwargs):
        """Start document after this"""
        if key:
            self._start_after = self._firestore_doc(key)
        else:
            self._start_after = self._fields_by_column_name(**kwargs)
        return self

    def start_at(self, key=None, **kwargs):
        """Start document at this point"""
        if key:
            self._start_at = self._firestore_doc(key)
        else:
            self._start_at = self._fields_by_column_name(**kwargs)
        return self

    def end_before(self, key=None, **kwargs):
        """End document before this point"""
        if key:
            self._end_before = self._firestore_doc(key)
        else:
            self._end_before = self._fields_by_column_name(**kwargs)
        return self

    def end_at(self, key=None, **kwargs):
        """End document at this point"""
        if key:
            self._end_at = self._firestore_doc(key)
        else:
            self._end_at = self._fields_by_column_name(**kwargs)
        return self

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
        if args:
            self.select_query.append(args)
        elif kwargs:
            for k, v in kwargs.items():
                self.select_query.append((k, '==', v))
        return self

    def limit(self, count):
        """Apply limit for query"""
        # save the Limit in cursor for next fetch
        self.cursor_dict['limit'] = count

        if count:
            self.n_limit = count
        return self

    def offset(self, num_to_skip):
        """Offset for query"""
        self._offset = num_to_skip
        return self

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
        # Save order in cursor dict for next fetch
        if 'order' in self.cursor_dict:
            self.cursor_dict['order'] = self.cursor_dict['order'] + ',' + field_name
        else:
            self.cursor_dict['order'] = field_name

        order_direction = 'Asc'
        name = field_name

        # If this is in Desc order
        if field_name[0] == '-':
            order_direction = 'Desc'
            name = field_name[1:]  # Get the field name after dash(-) e.g -age name will be age

        f_name = self._get_db_column_name(name)

        self.order_by.append((f_name, order_direction))
        return self

    def fetch(self, limit=None):
        """Fetch the result from firestore

        Parameters
        ---------
        limit : optional
            Apply limit to firestore documents, how much documents you want to retrieve
        """
        # save the Limit in cursor for next fetch
        self.cursor_dict['limit'] = limit

        if limit:
            self.n_limit = limit
        return QueryIterator(self)

    def group_fetch(self, limit=None):
        super().set_group_collection(True)
        return self.fetch(limit)

    def get(self):
        """Get the first matching document from firestore

        Get first matching document and convert it into model and return it
        This is same as `fetch(limit=1)` the only difference is `get()` method
        return **model instance** and the `fetch()` method return the **generator**
        """
        self.n_limit = 1
        doc = next(self.query().stream(self.query_transaction), None)
        if doc:
            m = query_wrapper.ModelWrapper.from_query_result(self.model, doc)
            m._update_doc = self._update_doc_key(m)
            return m
        return None

    def delete(self, child=False):
        """Delete the filter documents

        if child is True then delete nested collection and documents also
        """
        transaction_or_batch = self.query_transaction if self.query_transaction else self.query_batch
        q = self.query()
        DeleteQuery(self.model, query=q, child=child).exec(transaction_or_batch)

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
