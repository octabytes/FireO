import inspect

from fireo.database import db
from fireo.queries import query_result


class QuerySet:

    def __init__(self, model):
        self.model = model

    def create(self, **kwargs):
        return InsertQuery(self.model, **kwargs).exec()


class BaseQuery:

    def __init__(self, model):
        self.model = model

    def get_ref(self):
        ref = db.conn.collection(self.model.collection_name)
        return ref


class InsertQuery(BaseQuery):

    def __init__(self, model, **kwargs):
        super().__init__(model)
        self.query = kwargs
        if inspect.isclass(model):
            self.model = model()
            id_field = 'id'
            if model._meta.id is not None:
                id_field, _ = model._meta.id
            setattr(self.model, '_id', kwargs.get(id_field))

    def doc_ref(self):
        return self.get_ref().document(self.model._id)

    def parse_field(self):
        return {
            f.db_column_name: f.get_value(self.query.get(f.name))
            for f in self.model._meta.field_list.values()
        }

    def raw_exec(self):
        ref = self.doc_ref()
        ref.set(self.parse_field())
        return ref.get()

    def exec(self):
        return query_result.ModelFromDict.convert(self.model, self.raw_exec())
