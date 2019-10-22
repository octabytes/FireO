from fireo.queries import query_wrapper
from fireo.queries.base_query import BaseQuery
from fireo.queries.delete_query import DeleteQuery
from fireo.utils import utils
from google.cloud import firestore


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

    Methods
    -------
    parse_where():
        parse where filter

    query()
        Make a query that perform operation in firestore

    filter(args):
        Apply filter for querying document

    limit(n):
        Apply limit on number of documents

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

    def __init__(self, model_cls, parent=None, *args):
        super().__init__(model_cls)
        self.model = model_cls()
        self.select_query = [args] if args else []
        self.n_limit = None
        self.order_by = []
        self.parent = parent
        if parent:
            super().set_collection_path(path=parent)

    def parse_where(self):
        """Parse where filter

        User can change the field column name in firestore So, filter where clauses
        on the base of db column name
        """
        filters = []
        for w in self.select_query:
            name, op, val = w
            f_name = self.model._meta.get_field(name).db_column_name
            filters.append((f_name, op, val))
        return filters

    def query(self):
        """Make a query for firestore"""
        ref = self.get_ref()
        # parse where filter
        for f in self.parse_where():
            ref = ref.where(*f)
        # Apply limit
        if self.n_limit:
            ref = ref.limit(self.n_limit)
        # order the documents
        for o in self.order_by:
            name, direction = o
            if direction == 'Desc':
                ref = ref.order_by(name, direction=firestore.Query.DESCENDING)
            else:
                ref = ref.order_by(name)
        return ref

    def filter(self, *args):
        """Apply filter for querying document

        Apply where filter as many as you want

        Parameters
        ---------
        args: Tuple
            Contain three things 1- field name, 2-operation, 3-value

        Returns
        -------
        self:
            Return self object
        """
        self.select_query.append(args)
        return self

    def limit(self, limit):
        if limit:
            self.n_limit = limit
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
        order_direction = 'Asc'
        name = field_name

        # If this is in Desc order
        if field_name[0] == '-':
            order_direction = 'Desc'
            name = field_name[1:]  # Get the field name after dash(-) e.g -age name will be age
        f_name = self.model._meta.get_field(name).db_column_name
        self.order_by.append((f_name, order_direction))
        return self

    def fetch(self, limit=None):
        """Fetch the result from firestore

        Parameters
        ---------
        limit : optional
            Apply limit to firestore documents, how much documents you want to retrieve
        """
        if limit:
            self.n_limit = limit
        docs = self.query().stream()
        for doc in docs:
            m = query_wrapper.ModelWrapper.from_query_result(self.model, doc)
            m.update_doc = self._update_doc_key(m)
            yield m

    def get(self):
        """Get the first matching document from firestore

        Get first matching document and convert it into model and return it
        This is same as `fetch(limit=1)` the only difference is `get()` method
        return **model instance** and the `fetch()` method return the **generator**
        """
        self.n_limit = 1
        doc = next(self.query().stream(), None)
        if doc:
            m = query_wrapper.ModelWrapper.from_query_result(self.model, next(self.query().stream()))
            m.update_doc = self._update_doc_key(m)
            return m
        return None

    def delete(self):
        """Delete the filter documents"""
        q = self.query()
        DeleteQuery(self.model_cls, query=q).exec()

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
            update_doc_key = self.parent + '/' + utils.get_id(model.key)
        else:
            update_doc_key = model.key
        return update_doc_key