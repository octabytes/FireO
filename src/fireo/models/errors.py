"""Model related Errors"""


class NonAbstractModel(Exception):
    pass


class AbstractNotInstantiate(Exception):
    pass
