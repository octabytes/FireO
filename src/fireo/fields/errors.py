"""Field related errors"""

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

