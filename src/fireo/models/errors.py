"""Model related Errors"""
from typing import Tuple, TYPE_CHECKING

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


class ModelSerializingError(BaseModelError):
    def __init__(self, model: 'Model', field_path: 'Tuple[str, ...]', error: Exception):
        self.model = model
        self.field_path = field_path
        self.error_msg = str(error)
        self.original_error = error
        if isinstance(error, ModelSerializingError):
            self.field_path = (*self.field_path, *error.field_path)
            self.error_msg = error.error_msg
            self.original_error = error.original_error

    def __str__(self):
        key = self.model.key
        model_class = type(self.model)
        return (
            f"Cannot serialize model '{model_class.__module__}.{model_class.__qualname__}' "
            f"with key '{key}' due to error in field '{'.'.join(self.field_path)}': {self.error_msg}"
        )
