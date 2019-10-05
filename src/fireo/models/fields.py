from fireo.models.field_validation import FieldValidation


class Field:

    allowed_attributes = ['column_name']

    def __init__(self, *args, **kwargs):
        self.raw_attributes = kwargs
        self.name = None
        self.validation = FieldValidation(self, kwargs)

    def contribute_to_model(self, model_cls, name):
        self.name = name
        setattr(model_cls, name, None)
        model_cls._meta.add_field(self)

    @property
    def db_column_name(self):
        return self.raw_attributes.get("column_name") or self.name

    def get_value(self, val):
        v = self.validation.validate(val)
        return self.db_value(val)

    def db_value(self, val):
        return val

    def field_value(self, val):
        return val + "asdasd"


class IDField(Field):

    def contribute_to_model(self, model_cls, name):
        self.name = name
        setattr(model_cls, name, None)
        model_cls._meta.add_model_id(self)


class IntegerField(Field):
    pass


class StringField(Field):
    pass
