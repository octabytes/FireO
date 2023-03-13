import itertools
from typing import Optional, TYPE_CHECKING

from google.cloud.firestore_v1 import CollectionReference, Transaction

from fireo.queries import query_wrapper
from fireo.utils.cursor import Cursor

if TYPE_CHECKING:
    pass


class QueryIterator:
    """Iterator the documents coming from Firestore

    Iterate each document that is coming from Firestore and wrap it to the model
    QueryIterator also contain the other information for example Firestore query, cursor etc

    Methods
    -------
    fetch_next():
        Fetch next results
    """

    def __init__(
        self,
        model_cls,
        query: CollectionReference,
        query_transaction: Optional[Transaction],
        limit: Optional[int],
        cursor: Cursor,
    ):
        self.query = query
        self.model_cls = model_cls
        self.docs = query.stream(query_transaction)
        self.limit = limit

        # Get offset for next fetch
        self.offset = limit
        self._cursor = cursor
        self._cursor['offset'] = self.offset

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
                # Suppose this is last doc
                self.last_doc_key = m.key
                return m
            self.fetch_end = True
            # Save last doc key in cursor
            self._cursor['last_doc_key'] = self.last_doc_key
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
                q = self.query.start_after(self.last_doc)
            else:
                q = self.query.offset(self.offset)

            # Apply new Limit if there is any
            if limit:
                q = q.limit(limit)
                self.offset += limit
            else:
                self.offset += self.limit

            # Update offset in cursor
            self._cursor['offset'] = self.offset

            self.docs = itertools.chain(self.docs, q.stream())

    @property
    def cursor(self):
        return self._cursor.to_string()
