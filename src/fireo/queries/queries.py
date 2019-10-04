from fireo.database import db


class QuerySet:

    def __init__(self, model):
        self.model = model

    def create(self, **kwargs):
        return InsertQuery(self.model, **kwargs).exec()


class BaseQuery:

    def __init__(self, model):
        self.model = model

    def doc_ref(self):
        ref = db.conn.collection(self.model.collection_name).document(self.model.id)
        self.model.set_id(ref.id)
        return ref


class InsertQuery(BaseQuery):

    def __init__(self, model, **kwargs):
        super().__init__(model)
        self.fields = kwargs

    def raw_exec(self):
        ref = self.doc_ref()
        ref.set(self.fields)
        return ref.get()

    def exec(self):
        return self.raw_exec()
