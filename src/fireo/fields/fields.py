from fireo.database import db
from fireo.fields.base_field import Field
from fireo.fields import errors
from fireo.utils import utils
from google.cloud import firestore


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

    Methods
    -------
    attr_auto_load():
        Method for attribute auto_load

    Raises
    ------
    AttributeTypeError:
        If given type is not supported by attribute
    """

    allowed_attributes = ['auto_load']

    def __init__(self, model_ref, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Check model ref class is subclass for Model
        from fireo.models import Model
        if not issubclass(model_ref, Model):
            raise errors.ReferenceTypeError(f'Reference model {model_ref.__name__} must be inherit from Model class')
        self.model_ref = model_ref
        self.auto_load = True

    # Override method
    def field_value(self, val):
        v = self.field_attribute.parse(val)
        return v

    # Override method
    def db_value(self, model):
        # check reference model and passing model is same
        if not issubclass(model.__class__, self.model_ref):
            raise errors.ReferenceTypeError(f'Invalid reference type {self.name} required value type '
                                            f'field {self.model_ref.__name__}, but got {model.__class__.__name__}')
        # Get document reference from firestore
        return firestore.DocumentReference(*utils.ref_path(model.key), client=db.conn)

    def attr_auto_load(self, attr_val, field_val):
        """Attribute method for auto load

        Allow users to load reference documents automatically or just return the reference
        and user itself call the `get()` method to load the document.
        """
        if type(attr_val) is not bool:
            raise errors.AttributeTypeError(f'Attribute auto_load only accept bool type, got {type(attr_val)} in '
                                            f'model {self.model_cls.__name__} field {self.name}')
        self.auto_load = attr_val
        return field_val




class IDField(Field):
    """Specify custom id for models

    User can specify model id and will save with the same id in firestore otherwise it will
    return None and generate later from firestore and attached to model

    Example
    --------
    .. code-block:: python
        class User(Mode):
            user_id = IDField()

        u = User()
        u.user_id = "custom_doc_id"
        u.save()

        # After save id will be saved in `user_id`
        print(self.user_id)  # custom_doc_id
    """
    def contribute_to_model(self, model_cls, name):
        self.name = name
        setattr(model_cls, name, None)
        model_cls._meta.add_model_id(self)


class NumberField(Field):
    """Number field for Models

    Define numbers for models integer, float etc

    Examples
    --------
        class User(Model):
            age = NumberField()
    """
    pass


class TextField(Field):
    """Text field for Models

        Define text for models

        Examples
        --------
            class User(Model):
                age = TextField()
        """
    pass

