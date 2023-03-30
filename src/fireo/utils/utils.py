import re
from typing import List, Optional, Type, TYPE_CHECKING, Union

from google.cloud import firestore

from fireo.fields import Field

if TYPE_CHECKING:
    from fireo.models.model import Model


def collection_name(model):
    return re.sub('(?!^)([A-Z]+)', r'_\1', model).lower()


def ref_path(key):
    return key.split('/')


def collection_path(key):
    return '/'.join(key.split('/')[:-1])


def get_parent(key):
    return collection_path(key)


def get_parent_doc(key):
    return '/'.join(key.split('/')[:-2])


def get_id(key):
    try:
        return key.split('/')[-1]
    except AttributeError:
        return None


def get_key(collection: str, doc_id: str, parent_key: Optional[str] = None) -> str:
    """Get key for document."""
    assert not is_key(collection), 'Collection name cannot contain "/"'
    key = f'{collection}/{doc_id}'
    if parent_key:
        key = f'{parent_key}/{key}'

    return key


def GeoPoint(latitude: float, longitude: float):
    return firestore.GeoPoint(latitude, longitude)


def get_nested(dict, *args):
    if args and dict:
        element = args[0]
        if element:
            value = dict.get(element)
            return value if len(args) == 1 else get_nested(value, *args[1:])


def join_keys(first_arg, *args):
    """Join keys with dot.

    Example:
        >>> join_keys('a', 'b', 3, 'c')
        'a.b[3].c'
    """
    result = str(first_arg)
    for arg in args:
        if isinstance(arg, int):
            result += f'[{arg}]'
        else:
            result += f'.{arg}'

    return result


def get_flat_dict(dict_, prefix: str = None):
    """Get flat dict from nested dict by joining keys with dot.

    Example:
        >>> get_flat_dict({'a': 1, 'b': {'c': 2, 'd': {'e': 3}}})
        {'a': 1, 'b.c': 2, 'b.d.e': 3}
    """
    flat_dict = {}
    for key, value in dict_.items():
        if prefix:
            key = f'{prefix}.{key}'

        if isinstance(value, dict):
            flat_dict.update(get_flat_dict(value, key))
        else:
            flat_dict[key] = value
    return flat_dict


def is_key(key: str) -> bool:
    """Check if string is key."""
    if not isinstance(key, str):
        return False
    return "/" in key


def get_fields_for_path(
    model: 'Union[Model, Type[Model]]',
    root_field_name: str,
    *nested_fields_names: str,
) -> List[Field]:
    """Get fields for path."""
    from fireo.fields import MapField, NestedModelField
    from fireo.fields.errors import AttributeTypeError

    model_field: Field = model._meta.get_field(root_field_name)
    fields = [model_field]

    for p in nested_fields_names:
        if isinstance(model_field, NestedModelField):
            nested_model = model_field.nested_model
            model_field = nested_model._meta.get_field(p)
            fields.append(model_field)

        elif isinstance(model_field, MapField):
            break

        else:
            raise AttributeTypeError(f"Invalid field type: {model_field}")

    return fields


def get_db_column_names_for_path(
    model: 'Union[Model, Type[Model]]',
    root_field_name: str,
    *nested_fields_names: str,
) -> List[str]:
    """Get db column names for nested fields."""
    from fireo.fields import MapField

    fields = get_fields_for_path(model, root_field_name, *nested_fields_names)
    db_column_names = [f.db_column_name for f in fields]
    if isinstance(fields[-1], MapField):
        db_column_names.extend(nested_fields_names[len(fields) - 1:])

    return db_column_names


def get_dot_names_as_dot_columns(
    model: 'Union[Model, Type[Model]]',
    dotted_name: str,
) -> str:
    """Convert dotted names to db column names."""
    db_column_path = get_db_column_names_for_path(model, *dotted_name.split('.'))

    return '.'.join(db_column_path)


def get_nested_field_by_dotted_name(
    model: 'Union[Model, Type[Model]]',
    dotted_name: str,
) -> Field:
    """Get nested field by dotted name.

    Example:
        >>> class Nested(Model):
        ...     field = NumberField()
        >>>
        >>> class MyModel(Model):
        ...     nested = NestedModelField(Nested)
        >>>
        >>> get_nested_field_by_dotted_name(MyModel, 'nested.field')
        <fireo.fields.number.NumberField object at 0x7f8b8c0b7a90>
    """
    return get_fields_for_path(model, *dotted_name.split('.'))[-1]
