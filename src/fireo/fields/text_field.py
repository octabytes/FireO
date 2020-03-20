from fireo.fields import errors
from fireo.fields.base_field import Field
import re


class TextField(Field):
    """Text field for Models

    Define text for models

    allowed_attributes = ['max_length', 'to_lowercase']



    Examples
    --------
        class User(Model):
            age = TextField()
    """

    allowed_attributes = ['max_length', 'to_lowercase', 'format']

    def attr_format(self, attr_val, field_val):
        supported_types = ['title', 'upper', 'lower', 'capitalize']

        if attr_val in supported_types:
            if attr_val == 'title':
                return self._titlecase(field_val)
            if attr_val == 'upper':
                return field_val.upper()
            if attr_val == 'lower':
                return field_val.lower()
            if attr_val == 'capitalize':
                return field_val.capitalize()
        raise errors.AttributeTypeError(
            f'Invalid attribute type. Inside Field "{self.name}", "format" type must be one of them "{supported_types}".')

    def attr_max_length(self, attr_val, field_val):
        """Method for attribute max_length"""
        return field_val[:attr_val]

    def attr_to_lowercase(self, attr_val, field_val):
        """Method for attribute to_lowercase

            Convert text into lowercase
        """
        if attr_val:
            return field_val.lower()
        return field_val

    # override method
    def db_value(self, val):
        if type(val) is str or val is None:
            # check if user defined to set the value as lower case
            if self.model_cls._meta.to_lowercase:
                return val.lower()
            return val
        raise errors.InvalidFieldType(f'Invalid field type. Field "{self.name}" expected {str}, '
                                      f'got {type(val)}')

    def _titlecase(self, s):
        return re.sub(r"[A-Za-z]+('[A-Za-z]+)?",
                      lambda mo: mo.group(0)[0].upper() +
                                 mo.group(0)[1:].lower(),
                      s)
