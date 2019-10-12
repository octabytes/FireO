from fireo.queries import query_result
from fireo.queries.base_query import BaseQuery


class FilterQuery(BaseQuery):
    """Filter documents on the bases of where clauses

    Filter document by filed name, You can also sort and limit the documents.

    Methods
    -------
    parse_where():
        parse where filter

    query()
        Make a query that perform operation in firestore

    filter(args):
        Apply filter for querying document

    fetch(limit):
        Fetch document from firestore, limit is optional here

    get():
        Get the first matching document from firestore
    """

    def __init__(self, model_cls, *args):
        super().__init__(model_cls)
        self.model = model_cls()
        self.select_query = [args]
        self.limit = None

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
        if self.limit:
            ref = ref.limit(self.limit)
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

    def fetch(self, limit=None):
        """Fetch the result from firestore

        Parameters
        ---------
        limit : optional
            Apply limit to firestore documents, how much documents you want to retrieve
        """
        self.limit = limit
        docs = self.query().stream()
        for doc in docs:
            yield query_result.ModelFromResult.convert(self.model, doc)

    def get(self):
        """Get the first matching document from firestore

        Get first matching document and convert it into model and return it
        This is same as `fetch(limit=1)` the only difference is `get()` method
        return **model instance** and the `fetch()` method return the **generator**
        """
        self.limit = 1
        return query_result.ModelFromResult.convert(self.model, next(self.query().stream()))
