import re

from google.cloud import firestore


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


def GeoPoint(latitude: float, longitude: float):
    return firestore.GeoPoint(latitude, longitude)


def get_nested(dict, *args):
    if args and dict:
        element = args[0]
        if element:
            value = dict.get(element)
            return value if len(args) == 1 else get_nested(value, *args[1:])


def get_flat_dict(dict_):
    """Get flat dict from nested dict by joining keys with dot."""
    flat_dict = {}
    for key, value in dict_.items():
        if isinstance(value, dict):
            flat_dict.update({f'{key}.{k}': v for k, v in get_flat_dict(value).items()})
        else:
            flat_dict[key] = value
    return flat_dict


def generateKeyFromId(model, id):
    return model.collection_name + "/" + id


def isKey(str):
    return "/" in str


def remove_none_field(values):
    if isinstance(values, list):
        return [remove_none_field(v) for v in values]

    if not isinstance(values, dict):
        return values

    result = {}
    for k, v in values.items():
        if v is not None:
            if isinstance(v, (dict, list)):
                v = remove_none_field(v)

            result[k] = v

    return result
