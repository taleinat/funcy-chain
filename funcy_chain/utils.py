from collections.abc import Mapping, Set
from functools import reduce
from operator import itemgetter

__all__ = [
    "UNSET",
    "UnsetType",
    "make_func",
]


class UnsetType:
    def __repr__(self):
        return "<UNSET>"


UNSET = UnsetType()
UnsetType.__new__ = lambda: UNSET


def make_func(f, builtin=False, test=False):
    if callable(f):
        return f
    elif f is None:
        # pass None to builtin as predicate or mapping function for speed
        return None if builtin else bool if test else lambda x: x
    elif isinstance(f, (int, slice, str)):
        return itemgetter(f)
    elif isinstance(f, list):
        return lambda value: reduce(lambda obj, key: obj[key], f, value)
    elif isinstance(f, Mapping):
        return f.__getitem__
    elif isinstance(f, Set):
        return f.__contains__
    else:
        raise TypeError("Can't make a func from %s" % f.__class__.__name__)
