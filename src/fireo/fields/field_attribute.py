from copy import copy

from fireo.fields.errors import *


class FieldAttribute:
    """Parse the field attributes

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
        if no value is defined then default value is set for field

    default_factory:
        if no value is defined then default_factory is called to value set for field

    required:
        Required field if no value or default set raise an Error

    validator:
        Custom validation for field specify by user

    validator_kwargs:
        Optional extra parameters for validation on the field.

    Methods
    -------
    validate(value):
        validate the value and perform action according to attribute

    field_attr(attribute):
        Get value of field attribute

    call_attr_method(attr, value):
        Call method from field for custom attribute

    Raises
    ------
    AttributeError:
        if given attributes is not allowed in specific field

    RequiredField:
        If filed is required and no default and no value found

    FieldValidationFailed:
        if field not passed custom user defined validation

    AttributeMethodNotDefined:
        if any custom field not define the method for `allowed_attributes`
    """
    allowed_attributes = ['default', 'default_factory', 'required', 'column_name', 'validator', 'validator_kwargs']

    def __init__(self, field, attributes):
        self.field = field
        self.attributes = attributes or {}

    # validate each field and it's attributes
    def parse(self, value, ignore_required=False, ignore_default=False, run_only=None):
        """validate the value and perform action according to attribute"""
        for attr in self.attributes:
            if attr not in self.field.allowed_attributes + self.allowed_attributes:
                raise UnSupportedAttribute(f'"{self.field.__class__.__name__}" not support attribute {attr}')

            if run_only is not None:
                for attr in run_only:
                    if self.field_attr(attr) is not None:
                        value = self.call_attr_method(attr, value)

                # return the value back
                return value

            # check default value if set for field
            if value is None and not ignore_default:
                if self.default is not None:
                    value = copy(self.default)

                elif self.default_factory is not None:
                    value = self.default_factory()

            # check this field is required or not
            if self.required and value is None and not ignore_required:
                raise RequiredField(f'"{self.field.name}" is required for model {self.field.model_cls} '
                                    f'but received no default and no value.')

            # check if there any custom validation provided by user
            if self.validator is not None:
                if callable(self.validator):

                    # get response back from user defined method
                    # validate with validator_kwargs if provided, check TypeError due to argument mismatch 
                    if self.validator_kwargs is not None:
                        try:
                            validation_passed = self.validator(value, **self.validator_kwargs)
                        except TypeError:
                            raise FieldValidationFailed(f'"Validation failed due to argument mismatch with value "'
                                                        f' {value} and validator_kwargs {self.validator_kwargs}')
                    else:
                        validation_passed = self.validator(value)

                    # check type of response
                    if isinstance(validation_passed, bool):
                        if not validation_passed:
                            raise FieldValidationFailed(f'"{self.field.__class__.__name__}" failed validation'
                                                        f' with value {value}')
                    # if response type is tuple then unpack the response
                    # get the user defined error and show to user
                    if isinstance(validation_passed, tuple):
                        valid, error = validation_passed
                        if not valid:
                            raise FieldValidationFailed(f'"{self.field.__class__.__name__}" failed '
                                                        f'with {value}. {error}')
                else:
                    raise ValidatorNotCallable(f'Validator must be a callable, cannot be '
                                               f'{type(self.validator)} {self.validator}')

        # call those attributes method which are defined in this specific field
        # each field can specify any additional attributes
        for attr in self.field.allowed_attributes:
            if self.field_attr(attr) is not None and (value is not None or attr in self.field.empty_value_attributes):
                value = self.call_attr_method(attr, value)

        # return the value back
        return value

    def call_attr_method(self, attr, value):
        """Call method from field for custom attribute

        Any field which is extend from base `Field` and allow it's own attributes
        then attribute method should be defined for each attribute. And attribute
        method should return the value. if no value return then field value will set to None

        And each attribute must be start with the name `attr_` and then the name of attribute itself

            For example:
                for attribute **name** you need to must define method **attr_name()** otherwise it
                will raise `AttributeMethodNotDefined` exception

        Parameters:
        ----------
        attr_val:
            Attribute value that is define in field

        field_val:
            Field value that is define in model

        Return
        ------
        value:
            Modified or just the same value after performing action

        Raises
        ------
        AttributeMethodNotDefined:
            If method is not defined for attribute

        Examples:
        --------
        .. code-block:: python
            class HelloField(Field):
                allowed_attributes = ['if_startfrom']

                def attr_if_startfrom(self, attr_val, field_val)
                    if field_val.startswith(attr_val):
                        return "Hello" + field_val
                    return field_value


            class User(Model):
                name = HelloField(if_startfrom="A")

            u = User()
            u.name = "Azeem"

            # in this case attr_if_startfrom() method run and set the field value
            # as **Hello Azeem**

            u.save()
            print(u.name)  # Hello Azeem

        This is a way how you can create your own custom fields
        """

        try:
            # call attribute method from field
            return getattr(self.field, "attr_"+attr)(self.field_attr(attr), value)
        except AttributeError as e:
            raise AttributeMethodNotDefined(f'Method is not defined for attribute "{attr}" '
                                            f'in field "{self.field.__class__.__name__}"') from e

    def field_attr(self, attr):
        """Get value of field attribute"""
        return self.attributes.get(attr)

    @property
    def default(self):
        """if no value is define then default value is set for field"""
        return self.attributes.get('default')

    @property
    def default_factory(self):
        """if no value is define then default value is set for field"""
        return self.attributes.get('default_factory')

    @property
    def required(self):
        """Required field if no value or default set raise an Error"""
        return self.attributes.get("required")

    @property
    def validator(self):
        """Custom validation for field specify by user"""
        return self.attributes.get("validator")

    @property
    def validator_kwargs(self):
        """Custom validator kwargs for field"""
        return self.attributes.get("validator_kwargs")
