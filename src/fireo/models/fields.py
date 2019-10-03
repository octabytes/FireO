
class Field:

    def __init__(self):
        self.name = None

    def contribute_to_model(self, model, name):
        self.name = name
        setattr(model, name, None)
        model.meta.add_field(self)


class IntegerField(Field):
    pass


class StringField(Field):
    pass
