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
        Chain(data)
        .values()
        .map(lambda user_data: "{lastname}, {firstname}".format(**user_data))
        .sort()
    ).value
    assert names == ["Kennedy, Bob", "Liddle, Alice"]


def test_integers(Chain):
    assert (
        Chain([1, 2, 3, 7, 6, 5, 4])
        .without(3)
        .filter(lambda x: x > 2)
        .remove(lambda x: x > 6)
        .sort(reverse=True)
    ).value == [6, 5, 4]


def test_youngest(Chain):
    users = [
        {"user": "barney", "age": 36},
        {"user": "fred", "age": 40},
        {"user": "pebbles", "age": 1}
    ]
    assert (
        Chain(users)
        .sort("age")
        .map("user")
    ).value == ["pebbles", "barney", "fred"]
