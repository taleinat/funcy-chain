from funcy_chain import getter


def test_long_path(Chain):
    data = [{"a": {"b": {"c": [1, 2, {"d": [3, {1: 2}]}]}}}]
    assert Chain(data).map(getter(["a", "b", "c", 2, "d", 1, 1])).value == [2]


def test_names(Chain):
    data = {
        "user1": {
            "firstname": "Alice",
            "lastname": "Liddle",
        },
        "user2": {
            "firstname": "Bob",
            "lastname": "Kennedy",
        },
    }
    names = (
        Chain(data).items().map(getter([1, "lastname"], [1, "firstname"])).sort().map(", ".join)
    ).value
    assert names == ["Kennedy, Bob", "Liddle, Alice"]
