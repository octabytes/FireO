from typing import Any, Dict, Tuple


def resolve_meta_attr(name: str, bases: Tuple[type, ...], attrs: Dict[str, Any], default=None):
    """Find the first definition of an attribute according to MRO order."""
    if 'Meta' in attrs and hasattr(attrs['Meta'], name):
        return getattr(attrs['Meta'], name)

    for base in bases:
        if hasattr(base, '_meta'):
            meta = getattr(base, '_meta')
            if hasattr(meta, name):
                return getattr(meta, name, default)
    return default
