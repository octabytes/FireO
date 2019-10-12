"""Field related errors"""


class ReferenceTypeError(Exception):
    pass


class MissingFieldOptionError(Exception):
    pass


class FieldNotFound(Exception):
    pass


class RequiredField(Exception):
    pass


class FieldValidationFailed(Exception):
    pass


class ValidatorNotCallable(Exception):
    pass


class AttributeMethodNotDefined(Exception):
    pass

