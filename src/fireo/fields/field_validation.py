from fireo.fields.errors import RequiredField, FieldValidationFailed


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

    required:
        Required field if no value or default set raise an Error

    validator:
        Custom validation for field specify by user

    Methods
    -------
    validate(value):
        validate the value and perform action according to attribute
    """
    allowed_attributes = ['default', 'required', 'column_name', 'validator']

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
                raise RequiredField(f'{self.field.__class__.__name__} is required but received no default and no value.')

            # check if there any custom validation provided by user
            if self.validator is not None:
                if callable(self.validator):
                    # get response back from user defined method
                    validation_passed = self.validator()
                    # check type of response
                    if isinstance(validation_passed, bool):
                        if not validation_passed:
                            raise FieldValidationFailed(f'{self.field.__class__.__name__} failed validation with value {value}')
                    # if response type is tuple then unpack the response
                    # get the user defined error and show to user
                    if isinstance(validation_passed, tuple):
                        valid, error = validation_passed
                        if not valid:
                            raise FieldValidationFailed(f'{self.field.__class__.__name__} {error}')


    @property
    def default(self):
        """if no value is define then default value is set for field"""
        return self.attributes.get('default')

    @property
    def required(self):
        """Required field if no value or default set raise an Error"""
        return self.attributes.get("required")

    @property
    def validator(self):
        """Custom validation for field specify by user"""
        return self.attributes.get("validator")