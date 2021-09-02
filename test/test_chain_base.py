import heapq

from funcy_chain import chain


def test_empty_chain():
    assert chain([]) != []
    assert chain([]).value == []


def test_tap():
    arr = []
    assert chain([1, 2, 3]).tap(arr.append).value == [1, 2, 3]
    assert arr == [[1, 2, 3]]


def test_thru():
    assert chain([1, 3, 2]).thru(sorted).value == [1, 2, 3]
    assert chain([1, 3, 2]).thru(lambda arr: heapq.nlargest(2, arr)).value == [3, 2]
