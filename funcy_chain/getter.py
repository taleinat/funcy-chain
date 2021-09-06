from collections.abc import Mapping, Set
from functools import reduce
from operator import itemgetter


def getter(*get_exprs):
    if not get_exprs:
        raise TypeError("getter() takes at least 1 positional argument (0 given)")
    elif len(get_exprs) > 1:
        getters = tuple(map(getter, get_exprs))
        return lambda value: tuple(g(value) for g in getters)

    (expr,) = get_exprs
    if callable(expr):
        return expr
    elif isinstance(expr, (int, slice, str)):
        return itemgetter(expr)
    elif isinstance(expr, list):
        return lambda value: reduce(lambda obj, key: obj[key], expr, value)
    elif isinstance(expr, Mapping):
        return expr.__getitem__
    elif isinstance(expr, Set):
        return expr.__contains__
    else:
        raise TypeError("Can't make a getter from %s" % expr.__class__.__name__)
