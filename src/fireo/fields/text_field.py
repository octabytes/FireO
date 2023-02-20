from fireo.fields import errors
from fireo.fields.base_field import Field
import re

from fireo.utils.types import LoadOptions


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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.format_type = None
        self.supported_types = ['title', 'upper', 'lower', 'capitalize']

    def attr_format(self, attr_val, field_val):
        self.format_type = attr_val
        return field_val

    def attr_max_length(self, attr_val, field_val):
        """Method for attribute max_length"""
        return field_val[:attr_val]

    def attr_to_lowercase(self, attr_val, field_val):
        """Method for attribute to_lowercase

            Convert text into lowercase
        """
        if attr_val:
            return field_val.lower() if field_val is not None else None
        return field_val

    def _titlecase(self, s):
        return re.sub(r"[A-Za-z]+('[A-Za-z]+)?",
                      lambda mo: mo.group(0)[0].upper() +
                                 mo.group(0)[1:].lower(),
                      s)

    # override method
    def db_value(self, val):
        if type(val) is str or val is None:
            # check if user defined to set the value as lower case
            if self.model_cls._meta.to_lowercase:
                return val.lower() if val is not None else None
            return val
        raise errors.InvalidFieldType(f'Invalid field type. Field "{self.name}" expected {str}, '
                                      f'got {type(val)}')

    # override method
    def field_value(self, val, load_options=LoadOptions()):

        # check if val is None then there is no need to run these functions
        # just return back the None value
        if val is None:
            return val

        self.field_attribute.parse(val, run_only=['format'])
        if self.format_type:
            if self.format_type in self.supported_types:
                if self.format_type == 'title':
                    return self._titlecase(val)
                if self.format_type == 'upper':
                    return val.upper()
                if self.format_type == 'lower':
                    return val.lower()
                if self.format_type == 'capitalize':
                    return val.capitalize()
            raise errors.AttributeTypeError(
                f'Invalid attribute type. Inside Field "{self.name}", '
                f'"format" type must be one of them "{self.supported_types}".')
        return val
