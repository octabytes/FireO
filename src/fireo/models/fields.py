from fireo.models.field_validation import FieldValidation


class Field:

    def __init__(self, *args, **kwargs):
        self.name = None
        self.field_validation = FieldValidation(
            self, {
                attr: val for attr, val in kwargs if attr in FieldValidation.ATTRIBUTES
            }
        )

    def contribute_to_model(self, model, name):
        self.name = name
        setattr(model, name, None)
        model.meta.add_field(self)

    def check_value(self):
        pass


class IntegerField(Field):
    pass


class StringField(Field):
    pass
