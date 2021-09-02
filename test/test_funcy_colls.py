import pytest

from funcy_chain import chain


def test_join():
    chain([]).join().value  # Check that no exception is raised.
    assert chain(["a", "b"]).join().value == "ab"
    assert chain([[1], [2]]).join().value == [1, 2]
    assert chain([(1,), (2,)]).join().value == (1, 2)
    assert chain([{"a": 1, "b": 2}, {"b": -2, "c": 3}]).join().value == {"a": 1, "b": -2, "c": 3}
    assert chain([{"a": 1, "b": 2}, {"b": -2, "c": 3}]).merge().value == {"a": 1, "b": -2, "c": 3}


def test_join_with():
    chain([]).join_with(list).value  # Check that no exception is raised.
    assert chain([{"a": 1, "b": 2}, {"b": -2, "c": 3}]).join_with(list).value == {
        "a": [1],
        "b": [2, -2],
        "c": [3],
    }
    assert chain([{"a": 1, "b": 2}, {"b": -2, "c": 3}]).merge_with(list).value == {
        "a": [1],
        "b": [2, -2],
        "c": [3],
    }
    assert chain([{"a": 1, "b": 2}, {"b": -2, "c": 3}]).join_with(tuple).value == {
        "a": (1,),
        "b": (2, -2),
        "c": (3,),
    }


def test_walk():
    assert chain([1, 2]).walk(lambda x: x + 1).value == [2, 3]
    assert chain((1, 2)).walk(lambda x: x + 1).value == (2, 3)


def test_walk_keys():
    assert chain({1: 1, 2: 2}).walk_keys(lambda x: x + 1).value == {2: 1, 3: 2}


def test_walk_values():
    assert chain({1: 1, 2: 2}).walk_values(lambda x: x + 1).value == {1: 2, 2: 3}


def test_select():
    assert chain([]).select(lambda x: x > 1).value == []
    assert chain(()).select(lambda x: x > 1).value == ()
    assert chain([1, 2]).select(lambda x: x > 1).value == [2]
    assert chain((1, 2)).select(lambda x: x > 1).value == (2,)
    assert chain({1, 2}).select(lambda x: x > 1).value == {2}


def test_select_keys():
    assert chain({}).select_keys(lambda x: x > 1).value == {}
    assert chain({1: 1, 2: 2}).select_keys(lambda x: x > 1).value == {2: 2}


def test_select_values():
    assert chain({}).select_values(lambda x: x > 1).value == {}
    assert chain({1: 1, 2: 2}).select_values(lambda x: x > 1).value == {2: 2}


def test_compact():
    assert chain([]).compact().value == []
    assert chain(()).compact().value == ()
    assert chain({}).compact().value == {}
    assert chain([0, 2]).compact().value == [2]
    assert chain((0, 2)).compact().value == (2,)
    assert chain({0, 2}).compact().value == {2}
    assert chain({0: 1, 1: 0, 2: 2}).compact().value == {0: 1, 2: 2}


def test_flip():
    assert chain({}).flip().value == {}
    assert chain({1: 2}).flip().value == {2: 1}


def test_project():
    assert chain({}).project([]).value == {}
    assert chain({}).project([1]).value == {}
    assert chain({1: "a"}).project([1]).value == {1: "a"}
    assert chain({2: "b"}).project([1]).value == {}
    assert chain({1: "a", 2: "b"}).project([1]).value == {1: "a"}


def test_omit():
    assert chain({}).omit([]).value == {}
    assert chain({}).omit([1]).value == {}
    assert chain({1: "a"}).omit([1]).value == {}
    assert chain({2: "b"}).omit([1]).value == {2: "b"}
    assert chain({1: "a", 2: "b"}).omit([1]).value == {2: "b"}


def test_zip_values():
    assert chain([]).zip_values().value == []
    assert chain([{}]).zip_values().value == []
    assert chain([{1: "a"}]).zip_values().value == [("a",)]
    assert chain([{1: "a"}, {1: "aa"}]).zip_values().value == [("a", "aa")]
    assert chain([{1: "a"}, {2: "b"}]).zip_values().value == []
    assert chain([{1: "a", 2: "b"}, {1: "aa"}]).zip_values().sort().value == [("a", "aa")]
    assert chain([{1: "a", 2: "b"}, {2: "aa"}]).zip_values().sort().value == [("b", "aa")]


def test_zip_dicts():
    assert chain([]).zip_dicts().value == []
    assert chain([{}]).zip_dicts().value == []
    assert chain([{1: "a"}]).zip_dicts().value == [(1, ("a",))]
    assert chain([{1: "a"}, {1: "aa"}]).zip_dicts().value == [(1, ("a", "aa"))]
    assert chain([{1: "a"}, {2: "b"}]).zip_dicts().value == []
    assert chain([{1: "a", 2: "b"}, {1: "aa"}]).zip_dicts().sort().value == [(1, ("a", "aa"))]
    assert chain([{1: "a", 2: "b"}, {2: "aa"}]).zip_dicts().sort().value == [(2, ("b", "aa"))]


def test_where():
    assert chain([]).where(a=1).value == []
    assert chain([{}]).where(a=1).value == []
    assert chain([{"a": 1}]).where(a=1).value == [{"a": 1}]
    assert chain([{"a": 2}]).where(a=1).value == []
    assert chain([{"b": 1}]).where(a=1).value == []
    assert chain([{"a": 1}, {"a": 2}]).where(a=1).value == [{"a": 1}]


def test_pluck():
    assert chain([]).pluck("a").value == []
    with pytest.raises(KeyError):
        chain([{}]).pluck("a").value
    assert chain([{"a": 1}]).pluck("a").value == [1]
    with pytest.raises(KeyError):
        chain([{"a": 1}]).pluck("b").value
    assert chain([{"a": 1}, {"a": 2, "b": 3}]).pluck("a").value == [1, 2]


def test_pluck_attr():
    assert chain([]).pluck_attr("imag").value == []
    with pytest.raises(AttributeError):
        chain(["a"]).pluck_attr("imag").value
    assert chain([1j]).pluck_attr("imag").value == [1]
    with pytest.raises(AttributeError):
        chain([1j]).pluck_attr("foo").value
    assert chain([1j, 2j]).pluck_attr("imag").value == [1, 2]


def test_invoke():
    assert chain([]).invoke("foo").value == []
    assert chain([1j]).invoke("conjugate").value == [-1j]
    assert chain([[1, 2], [3, 4]]).invoke("count", 1).value == [1, 0]
