import abc

__all__ = [
    "ChainBase",
]


class ChainBase(metaclass=abc.ABCMeta):
    """Base class for method chaining implementations."""

    def __init__(self, value):
        self._value = value

    @property
    def value(self):
        return self._value

    def tap(self, interceptor):
        interceptor(self._value)
        return self

    def thru(self, interceptor):
        return self.__class__(interceptor(self._value))
