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