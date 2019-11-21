from fireo.fields import errors
from fireo.fields.base_field import Field


class TextField(Field):
    """Text field for Models

    Define text for models

    allowed_attributes = ['max_length']



    Examples
    --------
        class User(Model):
            age = TextField()
    """

    allowed_attributes = ['max_length']

    def attr_max_length(self, attr_val, field_val):
        """Method for attribute max_length"""
        return field_val[:attr_val]

    # override method
    def db_value(self, val):
        if type(val) is str or val is None:
            # check if user defined to set the value as lower case
            if self.model_cls._meta.to_lowercase:
                return val.lower()
            return val
        raise errors.InvalidFieldType(f'Invalid field type. Field "{self.name}" expected {str}, '
                                      f'got {type(val)}')
