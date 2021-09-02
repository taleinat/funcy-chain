import pytest

from funcy_chain import chain


def test_items():
    assert chain({}).items().value == []
    assert chain({1: 2}).items().value == [(1, 2)]

    with pytest.raises((AttributeError, TypeError)):
        assert chain([]).items().value


def test_keys():
    assert chain({}).keys().value == []
    assert chain({1: 2}).keys().value == [1]

    with pytest.raises((AttributeError, TypeError)):
        assert chain([]).keys().value


def test_values():
    assert chain({}).values().value == []
    assert chain({1: 2}).values().value == [2]

    with pytest.raises((AttributeError, TypeError)):
        assert chain([]).values().value


def test_update():
    assert chain({}).update().value == {}
    assert chain({}).update({"b": 2}).value == {"b": 2}
    assert chain({}).update([("b", 2)]).value == {"b": 2}
    assert chain({}).update(b=2).value == {"b": 2}
    assert chain({"a": 1}).update({"b": 2}).value == {"a": 1, "b": 2}
    assert chain({"a": 1}).update({"a": 2}).value == {"a": 2}

    with pytest.raises((AttributeError, TypeError)):
        assert chain([]).update().value
