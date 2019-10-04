from fireo.models.model_meta import ModelMeta
from fireo.queries.queries import QuerySet


class Model(metaclass=ModelMeta):

    # Get all the fields values from meta
    # which are attached with this mode
    # and convert them into corresponding db value
    # return dict {name: value}
    def database_values(self):
        return {
            f.db_column_name: f.get_value(getattr(self, f.name))
            for f in self._meta.field_list.values()
        }

    # Get model id
    @property
    def id(self):
        if self._meta.id is None:
            return None
        name, field = self._meta.id
        return field.get_value(getattr(self, name))

    def set_id(self, doc_id):
        id = 'id'
        if self._meta is not None:
            id, _ = self._meta.id
        setattr(self, id, doc_id)

    # Get collection name that is converting from model
    @property
    def collection_name(self):
        return self._meta.collection_name

    def save(self):
        q = QuerySet(self)
        q.create(**self.database_values())

