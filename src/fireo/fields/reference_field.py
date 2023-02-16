from fireo.database import db
from fireo.fields import errors
from fireo.fields.base_field import Field
from fireo.queries.query_wrapper import ReferenceDocLoader
from fireo.utils import utils
from google.cloud import firestore

from fireo.utils.types import LoadOptions


class ReferenceField(Field):
    """Reference of other model

    A DocumentReference refers to a document location in a Firestore database and
    can be used to write, read, or listen to the location. The document at the referenced
    location may or may not exist.

    Attributes
    ----------
    allowed_attribute: ['auto_load']
        Allow reference field to load automatically or not

    model_ref:
        Reference of the model

    auto_load:
        Reference field load setting, load it auto or not

    on_load:
        Call user specify method when reference document load

    Methods
    -------
    attr_auto_load():
        Method for attribute auto_load

    attr_on_load():
        Method for attribute on_load

    Raises
    ------
    AttributeTypeError:
        If given type is not supported by attribute
    """

    allowed_attributes = ['auto_load', 'on_load']

    empty_value_attributes = allowed_attributes

    def __init__(self, model_ref, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Check model ref class is subclass for Model
        from fireo.models import Model
        if not issubclass(model_ref, Model):
            raise errors.ReferenceTypeError(f'Reference model "{model_ref.__name__}" must be inherit from Model class')
        self.model_ref = model_ref
        self.auto_load = True
        self.on_load = None

    # Override method
    def field_value(self, val, load_options=LoadOptions()):
        ref = self.field_attribute.parse(val)

        if not ref:
            return None

        ref_doc = ReferenceDocLoader(load_options.model, self, ref)

        if self.auto_load:
            return ref_doc.get()

        return ref_doc

    # Override method
    def db_value(self, model):
        # if no model is provided then return None
        if model is None:
            return None
        # check reference model and passing model is same
        if not issubclass(model.__class__, self.model_ref):
            raise errors.ReferenceTypeError(f'Invalid reference type. Field "{self.name}" required value type '
                                            f'"{self.model_ref.__name__}", but got "{model.__class__.__name__}"')
        # Get document reference from firestore
        return firestore.DocumentReference(*utils.ref_path(model.key), client=db.conn)

    def attr_auto_load(self, attr_val, field_val):
        """Attribute method for auto load

        Allow users to load reference documents automatically or just return the reference
        and user itself call the `get()` method to load the document.
        """
        if type(attr_val) is not bool:
            raise errors.AttributeTypeError(f'Attribute auto_load only accept bool type, got {type(attr_val)} in '
                                            f'model "{self.model_cls.__name__}" field "{self.name}"')
        self.auto_load = attr_val
        return field_val

    def attr_on_load(self, method_name, field_val):
        """Attribute method for on load

        Call user specify method when reference document is loaded
        """
        try:
            m = getattr(self.model_cls, method_name)
            if not callable(m):
                raise errors.AttributeTypeError(f'Attribute {m} is not callable in model "{self.model_cls.__name__}" '
                                                f'field "{self.name}"')
            self.on_load = method_name
        except AttributeError as e:
            raise errors.AttributeMethodNotDefined(f'Method "{method_name}" is not defined for attribute on_load in '
                                                   f'model "{self.model_cls.__name__}" field "{self.name}"') from e

        return field_val
