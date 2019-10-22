"""Model related Errors"""


class UnSupportedMeta(Exception):
    pass


class NonAbstractModel(Exception):
    pass


class AbstractNotInstantiate(Exception):
    pass

