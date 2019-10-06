"""Field related errors"""


class RequiredField(Exception):
    pass


class FieldValidationFailed(Exception):
    pass
