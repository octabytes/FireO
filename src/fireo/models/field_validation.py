
class FieldValidation:

    ATTRIBUTES = {
        'default'
    }

    def __init__(self, field, attributes):
        self.field = field
        self.attributes = attributes or {}

