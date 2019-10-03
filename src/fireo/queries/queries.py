from fireo.database import db


class QuerySet:

    def __init__(self, model):
        self.model = model

    def create(self, **kwargs):
        pass


class BaseQuery:

    def __init__(self, model):
        self.model = model

    def doc_ref(self):
        return db.conn.collection("/".join(self.model.collection_name))


class InsertQuery(BaseQuery):

    def __init__(self, model, **kwargs):
        super().__init__(model)
        self.insert_fields = kwargs

