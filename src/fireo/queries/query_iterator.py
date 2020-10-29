import base64
import json
import itertools
from fireo.queries import query_wrapper


class QueryIterator:
    """Iterator the documents coming from Firestore

    Iterate each document that is coming from Firestore and wrap it to the model
    QueryIterator also contain the other information for example Firestore query, cursor etc

    Methods
    -------
    fetch_next():
        Fetch next results
    """

    def __init__(self, query):
        self.query = query
        self.model_cls = query.model.__class__
        self.docs = query.query().stream(query.query_transaction)
        # Get offset for next fetch
        self.offset = query.n_limit
        query.cursor_dict['offset'] = query.n_limit
        # Hold the last doc for next fetch
        self.last_doc = None
        self.last_doc_key = None
        self.fetch_end = False

    def __iter__(self):
        return self

    def __next__(self):
        try:
            doc = next(self.docs, None)
            if doc:
                # Suppose this is the last doc
                self.last_doc = doc
                m = query_wrapper.ModelWrapper.from_query_result(self.model_cls(), doc)
                m._update_doc = self.query._update_doc_key(m)
                # Suppose this is last doc
                self.last_doc_key = m.key
                return m
            self.fetch_end = True
            # Save last doc key in cursor
            self.query.cursor_dict['last_doc_key'] = self.last_doc_key
            raise StopIteration
        except StopIteration:
            raise StopIteration

    def next_fetch(self, limit=None):
        """Fetch next results"""

        # Make sure limit is apply in previous query otherwise there is no need to fetch next
        if self.offset:
            # check if fetch end then use last doc otherwise use the offset
            if self.fetch_end:
                self.fetch_end = False
                q = self.query.query().start_after(self.last_doc)
            else:
                q = self.query.query().offset(self.offset)

            # Apply new Limit if there is any
            if limit:
                q = q.limit(limit)
                self.offset += limit
            else:
                self.offset += self.query.n_limit

            # Update offset in cursor
            self.query.cursor_dict['offset'] = self.offset

            self.docs = itertools.chain(self.docs, q.stream())

    @property
    def cursor(self):
        encodedCursor = base64.b64encode(json.dumps(self.query.cursor_dict).encode('utf-8'))
        return str(encodedCursor, 'utf-8')
