from fireo.queries import query_wrapper
from fireo.queries.filter_query import FilterQuery


class QueryIterator:
    """Iterator the documents coming from Firestore

    Iterate each document that is coming from Firestore and wrap it to the model
    QueryIterator also contain the other information for example Firestore query, cursor etc
    """

    def __init__(self, query: FilterQuery):
        self.query = query
        self.docs = query.query().stream()

    def __next__(self):
        doc = next(self.docs, None)
        if doc:
            m = query_wrapper.ModelWrapper.from_query_result(self.query.model, doc)
            m.update_doc = self.query._update_doc_key(m)
            return m
        raise StopIteration
