from fireo.fields.errors import RequiredField


class FieldValidation:
    """Validate the field

    Check validation for fields and perform action according to field attributes

    Attributes
    ----------
    allowed_attributes : list
        Allowed attribute for each fields. This allow to add extra functionality for fields

        Examples
        ---------
        .. code-block:: python
            class User(Model):
                name = TextField(column_name="full_name")

        In firestore this fields will be store as **full_name**

    default:
        if no value is define then default value is set for field

    Methods
    -------
    validate(value):
        validate the value and perform action according to attribute
    """
    allowed_attributes = ['default','required','column_name']

    def __init__(self, field, attributes):
        self.field = field
        self.attributes = attributes or {}

    # validate each field and it's attributes
    def validate(self, value):
        """validate the value and perform action according to attribute"""
        for attr in self.attributes:
            if attr not in self.field.allowed_attributes + FieldValidation.allowed_attributes:
                raise AttributeError(f'{self.field.__class__.__name__} not allow attribute {attr}')

            # check default value if set for field
            if self.default is not None and value is None:
                value = self.default

            # check this field is required or not
            if self.required and value is None:
                raise RequiredField(f'{self.__class__.__name__} is required but received no default and no value.')

    @property
    def default(self):
        """if no value is define then default value is set for field"""
        return self.attributes.get('default')

    @property
    def required(self):
        """Required field if no value or default set raise an Error"""
        return self.attributes.get("required")
