from funcy_chain import Chain


def test_nlargest():
    assert Chain([]).nlargest(0).value == []
    assert Chain([]).nlargest(1).value == []
    assert Chain([1, 3, 2, 4, 3]).nlargest(2).value == [4, 3]
    assert Chain([1, 3, 2, 4, 3]).nlargest(3).value == [4, 3, 3]
    assert Chain([1, 3, 2, 4, 1]).nlargest(0).value == []


def test_nsmallest():
    assert Chain([]).nsmallest(0).value == []
    assert Chain([]).nsmallest(1).value == []
    assert Chain([1, 3, 2, 4, 1]).nsmallest(2).value == [1, 1]
    assert Chain([1, 3, 2, 4, 1]).nsmallest(3).value == [1, 1, 2]
    assert Chain([1, 3, 2, 4, 1]).nsmallest(0).value == []
