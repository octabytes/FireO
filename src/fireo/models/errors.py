"""Model related Errors"""
from typing import Tuple, TYPE_CHECKING

from fireo.utils.utils import join_keys

if TYPE_CHECKING:
    from fireo.models import Model


class BaseModelError(Exception):
    pass


class UnSupportedMeta(BaseModelError):
    pass


class NonAbstractModel(BaseModelError):
    pass


class AbstractNotInstantiate(BaseModelError):
    pass


class DuplicateIDField(BaseModelError):
    pass


class ModelSerializingWrappedError(BaseModelError):
    def __init__(self, model: 'Model', field_path: 'Tuple[str | int, ...]', error: Exception):
        self.model = model
        self.field_path = field_path
        self.original_error = error
        if isinstance(error, ModelSerializingWrappedError):
            self.field_path = (*self.field_path, *error.field_path)
            self.original_error = error.original_error

    def __str__(self):
        key = self.model.key
        model_class = type(self.model)
        path_str = join_keys(*self.field_path)
        return (
            f"Cannot serialize model '{model_class.__module__}.{model_class.__qualname__}' "
            f"with key '{key}' due to error in field '{path_str}': {self.original_error}"
        )
