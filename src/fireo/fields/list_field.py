from dataclasses import replace
from typing import Any, List, Optional

from google.cloud.firestore_v1 import ArrayRemove, ArrayUnion

from fireo.fields import errors, Field, IDField
from fireo.utils.types import DumpOptions, LoadOptions


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
    def get_value(self, val, dump_options=DumpOptions()):
        val = self.field_attribute.parse(val, dump_options.ignore_required, dump_options.ignore_default)

        if val is None:
            return None

        if type(val) not in [list, ArrayUnion, ArrayRemove]:
            raise errors.InvalidFieldType(f'Invalid field type. Field "{self.name}" expected {list}, '
                                          f'got {type(val)}')

        nested_field: Optional[Field] = self.raw_attributes.get('nested_field')
        if nested_field is not None:
            serialized_values = []
            for index, item in enumerate(val):
                try:
                    serialized_values.append(nested_field.get_value(
                        val=item,
                        dump_options=replace(
                            dump_options,
                            # ignore_unchanged used in update. Object nested in list cannot be updated partially
                            ignore_unchanged=False,
                        )
                    ))
                except Exception as error:
                    from fireo.models.errors import ModelSerializingWrappedError
                    raise ModelSerializingWrappedError(item, (index,), error) from error
        else:
            serialized_values = val

        return self.db_value(serialized_values)

    def db_value(self, val):
        # check if user defined to set the value as lower case
        if self.model_cls._meta.to_lowercase:
            return [v.lower() if type(v) is str else v for v in val]

        return val

    def field_value(self, val: Optional[List[Any]], load_options=LoadOptions()) -> Optional[List[Any]]:
        parsed = super().field_value(val, load_options)
        nested_field: Optional[Field] = self.raw_attributes.get('nested_field')

        if parsed is not None and nested_field is not None:
            parsed = [
                nested_field.field_value(item, replace(
                    load_options,
                    merge=False,  # merge is not supported for list items
                ))
                for item in parsed
            ]

        return parsed

    def contribute_to_model(self, model_cls, name):
        super().contribute_to_model(model_cls, name)
        nested_field: Optional[Field] = self.raw_attributes.get('nested_field')
        if nested_field is not None and isinstance(nested_field, Field):
            nested_field.name = name
            nested_field.model_cls = model_cls
