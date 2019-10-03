import re


def collection_name(model):
    return re.sub('(?!^)([A-Z]+)', r'_\1', model).lower()
