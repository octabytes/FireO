from fireo.fields import errors
from fireo.fields.base_field import Field


class NestedModel(Field):
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

