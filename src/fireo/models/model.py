from fireo.managers import managers
from fireo.models.model_meta import ModelMeta
from fireo.queries.queries import QuerySet


class Model(metaclass=ModelMeta):

    def __init__(self, *args, **kwargs):
        self.__class__.collection.initialize(self)
        for k, v in kwargs.items():
            setattr(self, k, v)

    # Get all the fields values from meta
    # which are attached with this mode
    # and convert them into corresponding db value
    # return dict {name: value}
    def _get_fields(self):
        return {
            f.name: getattr(self, f.name)
            for f in self._meta.field_list.values()
        }

    # def _database_values(self):
    #     return {
    #         f.db_column_name: f.get_value(getattr(self, f.name))
    #         for f in self._meta.field_list.values()
    #     }

    # Get model id
    @property
    def _id(self):
        if self._meta.id is None:
            return None
        name, field = self._meta.id
        return field.get_value(getattr(self, name))

    @_id.setter
    def _id(self, doc_id):
        id = 'id'
        if self._meta.id is not None:
            id, _ = self._meta.id
        setattr(self, id, doc_id)

    def save(self):
        return self.__class__.collection.create(**self._get_fields())

