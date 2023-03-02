from enum import Enum
from typing import Optional, Union

from fireo.fields import Field
from fireo.fields.errors import AttributeTypeError
from fireo.utils.types import LoadOptions


class EnumField(Field):
    allowed_attributes = ['enum']

    def __init__(self, enum, *args, **kwargs):
        if not isinstance(enum, type) or not issubclass(enum, Enum):
            raise AttributeTypeError('"enum" must be an subclass of "Enum".')

        super().__init__(*args, **kwargs, enum=enum)

    def attr_enum(self, attr_val, field_val):
        return field_val

    def db_value(self, val: Optional[Enum]) -> Union[str, int, None]:
        """Serialize enum by its value."""
        if isinstance(val, Enum):
            val = val.value

        return super().db_value(val)

    def field_value(self, val: Union[str, int, None], load_options=LoadOptions()) -> Optional[Enum]:
        """Deserialize enum from value"""
        parsed_value = super().field_value(val, load_options)

        parsed_enum = None
        if parsed_value is not None:
            parsed_enum = self.raw_attributes['enum'](parsed_value)

        return parsed_enum
