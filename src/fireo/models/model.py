from fireo.models.model_meta import ModelMeta


class Model(metaclass=ModelMeta):

    def fields_value(self):
        return {
            f.name: getattr(self, f.name)
            for f in self.meta.fields.values()
        }

    def save(self):
        print(self.fields_value())
