from typing import Optional, TYPE_CHECKING

from fireo.fields import errors
from fireo.fields.base_field import Field

if TYPE_CHECKING:
    from fireo.models import Model


class NestedModelField(Field):
    """Model inside another model"""

    def __init__(self, model, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Check nested model class is subclass for Model
        from fireo.models import Model
        if not issubclass(model, Model):
            raise errors.NestedModelTypeError(f'Nested model "{model.__name__}" must be inherit from Model class')
        self.nested_model = model

    def valid_model(self, model_instance):
        """Check nested model and passing model is same"""

        # return False if no Nested model apply
        if model_instance is None:
            return False

        if self.nested_model == model_instance.__class__:
            return True
        raise errors.NestedModelTypeError(f'Invalid nested model type. Field "{self.name}" required value type '
                                          f'"{self.nested_model.__name__}", but got '
                                          f'"{model_instance.__class__.__name__}"')

    def field_value(self, val, model):
        if not val:
            return None
        nested_model = self.nested_model()
        nested_model.populate_from_doc_dict(val)
        return nested_model

    def get_value(self, val: 'Optional[Model]', ignore_required=False, ignore_default=False, changed_only=False):
        if val is not None:
            val = val.to_db_dict(ignore_required, ignore_default, changed_only)
        val = self.field_attribute.parse(val, ignore_required, ignore_default)
        return self.db_value(val)


# NestedModel is deprecated. This name is now reserved for model that should be used as a nested model
NestedModel = NestedModelField
