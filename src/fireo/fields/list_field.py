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

    def __init__(self, nested_field=None, *args, **kwargs):
        kwargs['nested_field'] = nested_field
        super().__init__(*args, **kwargs)

    def attr_nested_field(self, attr_val, field_val):
        if attr_val is not None:
            if not isinstance(attr_val, Field):
                raise errors.AttributeTypeError(
                    f'Attribute nested_field only accept Field type, got {type(attr_val)} in '
                    f'model "{self.model_cls.__name__}" field "{self.name}"'
                )

            if isinstance(attr_val, (IDField, ListField)):
                raise errors.AttributeTypeError(
                    f'Attribute nested_field does not accept this type. '
                    f'Got {type(attr_val)} in model "{self.model_cls.__name__}" field "{self.name}"'
                )

        return field_val

    # Override method
    def get_value(self, val, ignore_required=False, ignore_default=False, changed_only=False):
        val = self.field_attribute.parse(val, ignore_required, ignore_default)

        if val is None:
            return None

        if type(val) not in [list, ArrayUnion, ArrayRemove]:
            raise errors.InvalidFieldType(f'Invalid field type. Field "{self.name}" expected {list}, '
                                          f'got {type(val)}')

        nested_field: Optional[Field] = self.raw_attributes.get('nested_field')
        if nested_field is not None:
            val = [
                nested_field.get_value(
                    val=item,
                    ignore_required=ignore_required,
                    ignore_default=ignore_default,
                    # changed_only used in update. Object nested in list cannot be updated partially
                    changed_only=False,
                )
                for item in val
            ]

        # check if user defined to set the value as lower case
        if self.model_cls._meta.to_lowercase:
            return [v.lower() if type(v) is str else v for v in val]

        return val

    def field_value(self, val: Optional[List[Any]], model) -> Optional[List[Any]]:
        """Deserialize enum from value"""
        parsed = super().field_value(val, model)
        nested_field: Optional[Field] = self.raw_attributes.get('nested_field')

        if parsed is not None and nested_field is not None:
            parsed = [nested_field.field_value(item, model) for item in parsed]

        return parsed

    def contribute_to_model(self, model_cls, name):
        super().contribute_to_model(model_cls, name)
        nested_field: Optional[Field] = self.raw_attributes.get('nested_field')
        if nested_field is not None and isinstance(nested_field, Field):
            nested_field.name = name
            nested_field.model_cls = model_cls
