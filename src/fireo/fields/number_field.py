from fireo.fields import errors
from fireo.fields.base_field import Field


class NumberField(Field):
    """Number field for Models

    Define numbers for models integer, float etc

    allowed_attributes = ['int_only', 'float_only']

    Examples
    --------
        class User(Model):
            age = NumberField()
    """

    allowed_attributes = ['int_only', 'float_only']

    def attr_int_only(self, attr_val, field_val):
        """Method for attribute int_only"""
        if attr_val and type(field_val) is not int:
            raise errors.InvalidFieldType(f'Invalid field type. Field "{self.name}" expected {int} type, '
                                          f'got {type(field_val)}')
        return field_val

    def attr_float_only(self, attr_val, field_val):
        """Method for attribute float_only"""
        if attr_val and type(field_val) is not float:
            raise errors.InvalidFieldType(f'Invalid field type. Field "{self.name}" expected {float} type, '
                                          f'got {type(field_val)}')
        return field_val

    # override method
    def db_value(self, val):
        if type(val) is int or type(val) is float or val is None:
            return val
        raise errors.InvalidFieldType(f'Invalid field type. Field "{self.name}" expected {int} or {float}, '
                                      f'got {type(val)}')