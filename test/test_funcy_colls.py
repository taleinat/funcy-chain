from test.conftest import IterChainWrapper

import pytest

from funcy_chain import IterChain


def test_join(Chain):
    Chain([]).join().value  # Check that no exception is raised.
    assert Chain(["a", "b"]).join().value == "ab"
    assert Chain([[1], [2]]).join().value == [1, 2]
    assert Chain([(1,), (2,)]).join().value == (1, 2)
    assert Chain([{"a": 1, "b": 2}, {"b": -2, "c": 3}]).join().value == {"a": 1, "b": -2, "c": 3}
    assert Chain([{"a": 1, "b": 2}, {"b": -2, "c": 3}]).merge().value == {"a": 1, "b": -2, "c": 3}


def test_join_with(Chain):
    Chain([]).join_with(list).value  # Check that no exception is raised.
    assert Chain([{"a": 1, "b": 2}, {"b": -2, "c": 3}]).join_with(list).value == {
        "a": [1],
        "b": [2, -2],
        "c": [3],
    }
    assert Chain([{"a": 1, "b": 2}, {"b": -2, "c": 3}]).merge_with(list).value == {
        "a": [1],
        "b": [2, -2],
        "c": [3],
    }
    assert Chain([{"a": 1, "b": 2}, {"b": -2, "c": 3}]).join_with(tuple).value == {
        "a": (1,),
        "b": (2, -2),
        "c": (3,),
    }


def test_walk(Chain):
    assert Chain([1, 2]).walk(lambda x: x + 1).value == [2, 3]
    assert Chain((1, 2)).walk(lambda x: x + 1).value == (2, 3)


def test_walk_keys(Chain):
    assert Chain({1: 1, 2: 2}).walk_keys(lambda x: x + 1).value == {2: 1, 3: 2}


def test_walk_values(Chain):
    assert Chain({1: 1, 2: 2}).walk_values(lambda x: x + 1).value == {1: 2, 2: 3}


def test_select(Chain):
    assert Chain([]).select(lambda x: x > 1).value == []
    assert Chain([1, 2]).select(lambda x: x > 1).value == [2]
    if not issubclass(Chain, IterChainWrapper):
        assert Chain(()).select(lambda x: x > 1).value == ()
        assert Chain((1, 2)).select(lambda x: x > 1).value == (2,)
        assert Chain({1, 2}).select(lambda x: x > 1).value == {2}


def test_select_keys(Chain):
    assert Chain({}).select_keys(lambda x: x > 1).value == {}
    assert Chain({1: 1, 2: 2}).select_keys(lambda x: x > 1).value == {2: 2}


def test_select_values(Chain):
    assert Chain({}).select_values(lambda x: x > 1).value == {}
    assert Chain({1: 1, 2: 2}).select_values(lambda x: x > 1).value == {2: 2}


def test_compact(Chain):
    assert Chain([]).compact().value == []
    if not issubclass(Chain, IterChainWrapper):
        assert Chain(()).compact().value == ()
        assert Chain({}).compact().value == {}
    assert Chain([0, 2]).compact().value == [2]
    if not issubclass(Chain, IterChainWrapper):
        assert Chain((0, 2)).compact().value == (2,)
        assert Chain({0, 2}).compact().value == {2}
        assert Chain({0: 1, 1: 0, 2: 2}).compact().value == {0: 1, 2: 2}


def test_flip(Chain):
    assert Chain({}).flip().value == {}
    assert Chain({1: 2}).flip().value == {2: 1}


def test_project(Chain):
    assert Chain({}).project([]).value == {}
    assert Chain({}).project([1]).value == {}
    assert Chain({1: "a"}).project([1]).value == {1: "a"}
    assert Chain({2: "b"}).project([1]).value == {}
    assert Chain({1: "a", 2: "b"}).project([1]).value == {1: "a"}


def test_omit(Chain):
    assert Chain({}).omit([]).value == {}
    assert Chain({}).omit([1]).value == {}
    assert Chain({1: "a"}).omit([1]).value == {}
    assert Chain({2: "b"}).omit([1]).value == {2: "b"}
    assert Chain({1: "a", 2: "b"}).omit([1]).value == {2: "b"}


def test_zip_values(Chain):
    assert Chain([]).zip_values().value == []
    assert Chain([{}]).zip_values().value == []
    assert Chain([{1: "a"}]).zip_values().value == [("a",)]
    assert Chain([{1: "a"}, {1: "aa"}]).zip_values().value == [("a", "aa")]
    assert Chain([{1: "a"}, {2: "b"}]).zip_values().value == []
    assert Chain([{1: "a", 2: "b"}, {1: "aa"}]).zip_values().sort().value == [("a", "aa")]
    assert Chain([{1: "a", 2: "b"}, {2: "aa"}]).zip_values().sort().value == [("b", "aa")]


def test_zip_dicts(Chain):
    assert Chain([]).zip_dicts().value == []
    assert Chain([{}]).zip_dicts().value == []
    assert Chain([{1: "a"}]).zip_dicts().value == [(1, ("a",))]
    assert Chain([{1: "a"}, {1: "aa"}]).zip_dicts().value == [(1, ("a", "aa"))]
    assert Chain([{1: "a"}, {2: "b"}]).zip_dicts().value == []
    assert Chain([{1: "a", 2: "b"}, {1: "aa"}]).zip_dicts().sort().value == [(1, ("a", "aa"))]
    assert Chain([{1: "a", 2: "b"}, {2: "aa"}]).zip_dicts().sort().value == [(2, ("b", "aa"))]


def test_where(Chain):
    assert Chain([]).where(a=1).value == []
    assert Chain([{}]).where(a=1).value == []
    assert Chain([{"a": 1}]).where(a=1).value == [{"a": 1}]
    assert Chain([{"a": 2}]).where(a=1).value == []
    assert Chain([{"b": 1}]).where(a=1).value == []
    assert Chain([{"a": 1}, {"a": 2}]).where(a=1).value == [{"a": 1}]


def test_pluck(Chain):
    assert Chain([]).pluck("a").value == []
    with pytest.raises(KeyError):
        Chain([{}]).pluck("a").value
    assert Chain([{"a": 1}]).pluck("a").value == [1]
    with pytest.raises(KeyError):
        Chain([{"a": 1}]).pluck("b").value
    assert Chain([{"a": 1}, {"a": 2, "b": 3}]).pluck("a").value == [1, 2]


def test_pluck_attr(Chain):
    if issubclass(Chain, IterChainWrapper):
        Chain = IterChain
    assert list(Chain([]).pluck_attr("imag").value) == []
    with pytest.raises(AttributeError):
        list(Chain(["a"]).pluck_attr("imag").value)
    assert list(Chain([1j]).pluck_attr("imag").value) == [1]
    with pytest.raises(AttributeError):
        list(Chain([1j]).pluck_attr("foo").value)
    assert list(Chain([1j, 2j]).pluck_attr("imag").value) == [1, 2]


def test_invoke(Chain):
    assert Chain([]).invoke("foo").value == []
    assert Chain([1j]).invoke("conjugate").value == [-1j]
    assert Chain([[1, 2], [3, 4]]).invoke("count", 1).value == [1, 0]
