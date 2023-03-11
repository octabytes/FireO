from google.cloud.firestore_v1.transforms import _NumericValue

from fireo.fields import errors
from fireo.fields.base_field import Field


class NumberField(Field):
    """Number field for Models

    Define numbers for models integer, float etc

    allowed_attributes = ['int_only', 'float_only', range]

    Examples
    --------
        class User(Model):
            age = NumberField()
    """

    allowed_attributes = ['int_only', 'float_only', 'range']

    def attr_range(self, attr_val, field_val):
        """Method for attribute range"""
        try:
            start, stop = attr_val
        except TypeError:
            start = attr_val
            stop = None

        if start and field_val < start:
            raise errors.NumberRangeError(f'Field "{self.name}" expect number must be grater or equal '
                                          f'than {start}, given {field_val}')
        if stop and field_val > stop:
            raise errors.NumberRangeError(f'Field "{self.name}" expect number must be less than or equal '
                                          f'to {stop}, given {field_val}')

        return field_val

    def attr_int_only(self, attr_val, field_val):
        """Method for attribute int_only"""
        if attr_val is not None and not isinstance(get_real_value(field_val), int):
            raise errors.InvalidFieldType(f'Invalid field type. Field "{self.name}" expected {int} type, '
                                          f'got {type(field_val)}')
        return field_val

    def attr_float_only(self, attr_val, field_val):
        """Method for attribute float_only"""
        if attr_val is not None and not isinstance(get_real_value(field_val), float):
            raise errors.InvalidFieldType(f'Invalid field type. Field "{self.name}" expected {float} type, '
                                          f'got {type(field_val)}')
        return field_val

    # override method
    def db_value(self, val):
        if isinstance(val, str):
            # Allow using string values for numbers. In filters as well.
            org_val = val
            try:
                if not self.raw_attributes.get('int_only'):
                    val = float(org_val)
                if not self.raw_attributes.get('float_only'):
                    val = int(org_val)
            except ValueError:
                pass

        if isinstance(get_real_value(val), (int, float)) or val is None:
            return val
        raise errors.InvalidFieldType(f'Invalid field type. Field "{self.name}" expected {int} or {float}, '
                                      f'got {type(val)}')


def get_real_value(val):
    if isinstance(val, _NumericValue):
        return val.value
    return val
