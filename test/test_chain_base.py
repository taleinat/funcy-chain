import heapq

from funcy_chain import Chain


def test_empty_chain():
    assert Chain([]) != []
    assert Chain([]).value == []


def test_tap():
    arr = []
    assert Chain([1, 2, 3]).tap(arr.append).value == [1, 2, 3]
    assert arr == [[1, 2, 3]]


def test_thru():
    assert Chain([1, 3, 2]).thru(sorted).value == [1, 2, 3]
    assert Chain([1, 3, 2]).thru(lambda arr: heapq.nlargest(2, arr)).value == [3, 2]
