import sys
from test.conftest import IterChainWrapper

import pytest


def test_enumerate(Chain):
    assert Chain([]).enumerate().value == []
    assert Chain([1, 2, 3]).enumerate().value == [(0, 1), (1, 2), (2, 3)]


def test_max(Chain):
    assert Chain([1, 3, 2]).max().value == 3
    assert Chain([1, 3, 2]).max(key=lambda x: -x).value == 1

    with pytest.raises(ValueError):
        Chain([]).max()


def test_min(Chain):
    assert Chain([1, 3, 2]).min().value == 1
    assert Chain([1, 3, 2]).min(key=lambda x: -x).value == 3

    with pytest.raises(ValueError):
        Chain([]).min()


def test_reduce(Chain):
    add = lambda a, b: a + b

    # empty lists
    assert Chain([]).reduce(add, 0).value == 0
    assert Chain([]).reduce(add, []).value == []
    with pytest.raises(Exception):
        Chain([]).reduce(add).value

    # adding ints
    assert Chain([1, 2, 3]).reduce(add).value == 6
    assert Chain([1, 2, 3]).reduce(add, 0).value == 6
    assert Chain([1, 2, 3]).reduce(add, 4).value == 10

    # list concatenation
    assert Chain([[1], [2]]).reduce(add).value == [1, 2]
    assert Chain([[1], [2]]).reduce(add, []).value == [1, 2]
    with pytest.raises(TypeError):
        Chain([[1], [2]]).reduce(add, 0).value


def test_reverse(Chain):
    assert Chain([]).reverse().value == []
    assert Chain([1, 2, 3]).reverse().value == [3, 2, 1]
    assert Chain([1, 2, 3]).reverse().reverse().value == [1, 2, 3]
    assert Chain([[1], [2]]).reverse().value == [[2], [1]]


def test_slice(Chain):
    assert Chain([]).slice(1).value == []
    assert Chain([1, 2, 3]).slice(3).value == [1, 2, 3]
    assert Chain([1, 2, 3]).slice(0, 3).value == [1, 2, 3]
    assert Chain([1, 2, 3]).slice(2).value == [1, 2]
    assert Chain([1, 2, 3]).slice(0, 2).value == [1, 2]
    assert Chain([1, 2, 3]).slice(1, 3).value == [2, 3]
    assert Chain([1, 2, 3]).slice(1, None).value == [2, 3]
    assert Chain([1, 2, 3]).slice(2, None).value == [3]
    assert Chain([1, 2, 3]).slice(3, None).value == []
    assert Chain([1, 2, 3]).slice(4, None).value == []
    assert Chain([1, 2, 3]).slice(1, 2).value == [2]
    assert Chain([1, 2, 3]).slice(0, 3).value == [1, 2, 3]

    assert Chain([1, 2, 3, 4, 5, 6, 7, 8]).slice(0, 8, 2).value == [1, 3, 5, 7]

    if not issubclass(Chain, IterChainWrapper):
        assert Chain([1, 2, 3]).slice(0, 3, -1).value == []
        assert Chain([1, 2, 3]).slice(3, 0, -1).value == [3, 2]
        assert Chain([1, 2, 3]).slice(3, None, -1).value == [3, 2, 1]
        assert Chain([1, 2, 3]).slice(0, -1).value == [1, 2]
        assert Chain([1, 2, 3]).slice(1, -1).value == [2]
        assert Chain([1, 2, 3]).slice(-1, 3).value == [3]
        assert Chain([1, 2, 3]).slice(-1, 1).value == []
        assert Chain([1, 2, 3, 4, 5, 6, 7, 8]).slice(8, None, -2).value == [8, 6, 4, 2]
        assert Chain([1, 2, 3, 4, 5, 6, 7, 8]).slice(8, 2, -2).value == [8, 6, 4]


def test_sort(Chain):
    assert Chain([]).sort().value == []
    assert Chain([1, 3, 2]).sort().value == [1, 2, 3]
    assert Chain([1, 3, 2]).sort(reverse=True).value == [3, 2, 1]
    assert Chain([1, 3, 2]).sort(key=lambda x: -x).value == [3, 2, 1]
    assert Chain([1, 3, 2]).sort(key=lambda x: -x, reverse=True).value == [1, 2, 3]
    assert Chain([1, 3, 2]).sort(lambda x: -x, True).value == [1, 2, 3]


def test_sum(Chain):
    assert Chain([]).sum().value == 0
    assert Chain([1, 3, 2]).sum().value == 6
    assert Chain([1, 3, 2]).sum(4).value == 10
    assert Chain([1, 3, 2]).sum(start=4).value == 10

    with pytest.raises(TypeError):
        Chain([[1], [2]]).sum().value
    assert Chain([[1], [2]]).sum([]).value == [1, 2]
    assert Chain([[1], [2]]).sum(start=[]).value == [1, 2]


def test_zip(Chain):
    assert Chain([]).zip().value == []
    assert Chain([()]).zip().value == []
    assert Chain([(), ()]).zip().value == []
    assert Chain([(1,), (3,)]).zip().value == [(1, 3)]
    assert Chain([(1, 2)]).zip().value == [(1,), (2,)]
    assert Chain([(1, 2), ()]).zip().value == []
    assert Chain([(1, 2), (3,)]).zip().value == [(1, 3)]
    assert Chain([(1,), (3, 4)]).zip().value == [(1, 3)]
    assert Chain([(1, 2), (3, 4)]).zip().value == [(1, 3), (2, 4)]

    if sys.version_info >= (3, 10):
        with pytest.raises(ValueError):
            Chain([(1, 2), ()]).zip(strict=True).value
        with pytest.raises(ValueError):
            Chain([(1, 2), (3,)]).zip(strict=True).value
        with pytest.raises(ValueError):
            Chain([(1,), (3, 4)]).zip(strict=True).value
