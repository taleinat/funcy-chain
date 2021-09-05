import functools
import itertools
from collections.abc import Collection, Iterable, MappingView, Sequence

import pytest

from funcy_chain import Chain as _Chain
from funcy_chain import IterChain


class IterChainWrapper:
    """Wrapper for testing IterChain identically to Chain."""

    def __init__(self, value):
        self._iterchain = IterChain(value)

    @classmethod
    def from_iterchain(self, iterchain):
        return IterChainWrapper(iterchain._value)

    @property
    def value(self):
        value = self._iterchain.value
        if isinstance(value, Iterable) and (
            isinstance(value, MappingView) or not isinstance(value, Collection)
        ):
            value = list(value)
        return value

    def __getattr__(self, name):
        attr = getattr(self._iterchain, name)
        if callable(attr):

            @functools.wraps(attr)
            def new_method(*args, **kwargs):
                return IterChainWrapper.from_iterchain(attr(*args, **kwargs))

            return new_method
        return attr


@pytest.fixture(scope="session", params=[_Chain, IterChainWrapper])
def Chain(request):
    return request.param
