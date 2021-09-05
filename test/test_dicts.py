import pytest

from funcy_chain import Chain


def test_items():
    assert Chain({}).items().value == []
    assert Chain({1: 2}).items().value == [(1, 2)]

    with pytest.raises((AttributeError, TypeError)):
        assert Chain([]).items().value


def test_keys():
    assert Chain({}).keys().value == []
    assert Chain({1: 2}).keys().value == [1]

    with pytest.raises((AttributeError, TypeError)):
        assert Chain([]).keys().value


def test_values():
    assert Chain({}).values().value == []
    assert Chain({1: 2}).values().value == [2]

    with pytest.raises((AttributeError, TypeError)):
        assert Chain([]).values().value


def test_update():
    assert Chain({}).update().value == {}
    assert Chain({}).update({"b": 2}).value == {"b": 2}
    assert Chain({}).update([("b", 2)]).value == {"b": 2}
    assert Chain({}).update(b=2).value == {"b": 2}
    assert Chain({"a": 1}).update({"b": 2}).value == {"a": 1, "b": 2}
    assert Chain({"a": 1}).update({"a": 2}).value == {"a": 2}

    with pytest.raises((AttributeError, TypeError)):
        assert Chain([]).update().value
