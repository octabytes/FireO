from fireo.models.model_meta import ModelMeta


class Model(metaclass=ModelMeta):

    # Get all the fields values from meta
    # which are attached with this mode
    # return dict {name: value}
    def fields_value(self):
        return {
            f.name: getattr(self, f.name)
            for f in self.meta.fields.values()
        }

    # Get collection name that is converting from model
    @property
    def collection_name(self):
        return self.meta.collection_name

    def save(self):
        print(self.fields_value())

    @classmethod
    def get_f(cls):
        print(cls.meta.fields)

    def get_f2(self):
        print(self.meta.fields)
