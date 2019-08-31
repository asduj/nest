__all__ = [
    'NestException',
    'InputFormatError',
    'LimitedKeysNumberError',
    'CompositeValueError',
]


class NestException(Exception):
    pass


class InputFormatError(NestException):
    pass


class LimitedKeysNumberError(NestException):
    pass


class CompositeValueError(NestException):
    pass
