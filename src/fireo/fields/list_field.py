from typing import Any, List, Optional

from google.cloud.firestore_v1 import ArrayRemove, ArrayUnion

from fireo.fields import errors, Field, IDField


class ListField(Field):
    """Array field for firestore

    Example
    -------
        class User(Model):
            subjects = ListField()

        u = User()
        u.subjects = ['English', 'Math']
    """

    allowed_attributes = ['nested_field']

    def attr_nested_field(self, attr_val, field_val):
        if attr_val is not None:
            if not isinstance(attr_val, Field):
                raise errors.AttributeTypeError(
                    f'Attribute nested_field only accept Field type, got {type(attr_val)} in '
                    f'model "{self.model_cls.__name__}" field "{self.name}"'
                )

            if isinstance(attr_val, (ListField, IDField)):
                raise errors.AttributeTypeError(
                    f'Attribute nested_field does not accept this type. '
                    f'Got {type(attr_val)} in model "{self.model_cls.__name__}" field "{self.name}"'
                )

            from fireo.fields import NestedModel
            if isinstance(attr_val, NestedModel):
                raise errors.AttributeTypeError(
                    f'Attribute nested_field currently has no implementation for this type. '
                    f'Got {type(attr_val)} in model "{self.model_cls.__name__}" field "{self.name}"'
                )

        return field_val

    # Override method
    def db_value(self, val):
        if val is None:
            return None

        if type(val) not in [list, ArrayUnion, ArrayRemove]:
            raise errors.InvalidFieldType(f'Invalid field type. Field "{self.name}" expected {list}, '
                                          f'got {type(val)}')

        nested_field: Optional[Field] = self.raw_attributes.get('nested_field')
        if nested_field is not None:
            val = [nested_field.db_value(item) for item in val]

        # check if user defined to set the value as lower case
        if self.model_cls._meta.to_lowercase:
            return [v.lower() if type(v) is str else v for v in val]

        return val

    def field_value(self, val: Optional[List[Any]]) -> Optional[List[Any]]:
        """Deserialize enum from value"""
        parsed = super().field_value(val)
        nested_field: Optional[Field] = self.raw_attributes.get('nested_field')

        if parsed is not None and nested_field is not None:
            parsed = [nested_field.field_value(item) for item in parsed]

        return parsed
