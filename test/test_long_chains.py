from funcy_chain import chain


def test_names():
    data = {
        "user1": {
            "firstname": "Alice",
            "lastname": "Liddle",
        },
        "user2": {
            "firstname": "Bob",
            "lastname": "Kennedy",
        }
    }
    names = (
        chain(data)
            .values()
            .map(lambda user_data: "{lastname}, {firstname}".format(**user_data))
            .sort()
    ).value
    assert names == ["Kennedy, Bob", "Liddle, Alice"]


def test_integers():
    assert (
        chain([1, 2, 3, 7, 6, 5, 4])
            .without(3)
            .filter(lambda x: x > 2)
            .remove(lambda x: x > 6)
            .sort(reverse=True)
    ).value == [6, 5, 4]
