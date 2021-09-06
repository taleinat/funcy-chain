from collections.abc import Mapping, Set
from functools import reduce
from operator import itemgetter

__all__ = [
    "UNSET",
    "UnsetType",
]


class UnsetType:
    def __repr__(self):
        return "<UNSET>"


UNSET = UnsetType()
UnsetType.__new__ = lambda: UNSET
