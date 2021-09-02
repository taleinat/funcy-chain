import pytest

from funcy_chain import chain


def test_enumerate():
    assert chain([]).enumerate().value == []
    assert chain([1, 2, 3]).enumerate().value == [(0, 1), (1, 2), (2, 3)]


def test_max():
    assert chain([1, 3, 2]).max().value == 3
    assert chain([1, 3, 2]).max(key=lambda x: -x).value == 1

    with pytest.raises(ValueError):
        chain([]).max()


def test_min():
    assert chain([1, 3, 2]).min().value == 1
    assert chain([1, 3, 2]).min(key=lambda x: -x).value == 3

    with pytest.raises(ValueError):
        chain([]).min()


def test_sort():
    assert chain([]).sort().value == []
    assert chain([1, 3, 2]).sort().value == [1, 2, 3]
    assert chain([1, 3, 2]).sort(reverse=True).value == [3, 2, 1]
    assert chain([1, 3, 2]).sort(key=lambda x: -x).value == [3, 2, 1]
    assert chain([1, 3, 2]).sort(key=lambda x: -x, reverse=True).value == [1, 2, 3]
    assert chain([1, 3, 2]).sort(lambda x: -x, True).value == [1, 2, 3]


def test_reduce():
    add = lambda a, b: a + b

    # empty lists
    assert chain([]).reduce(add, 0).value == 0
    assert chain([]).reduce(add, []).value == []
    with pytest.raises(Exception):
        chain([]).reduce(add).value

    # adding ints
    assert chain([1, 2, 3]).reduce(add).value == 6
    assert chain([1, 2, 3]).reduce(add, 0).value == 6
    assert chain([1, 2, 3]).reduce(add, 4).value == 10

    # list concatenation
    assert chain([[1], [2]]).reduce(add).value == [1, 2]
    assert chain([[1], [2]]).reduce(add, []).value == [1, 2]
    with pytest.raises(TypeError):
        chain([[1], [2]]).reduce(add, 0).value


def test_reverse():
    assert chain([]).reverse().value == []
    assert chain([1, 2, 3]).reverse().value == [3, 2, 1]
    assert chain([1, 2, 3]).reverse().reverse().value == [1, 2, 3]
    assert chain([[1], [2]]).reverse().value == [[2], [1]]
