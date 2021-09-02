from funcy_chain import chain


def test_nlargest():
    assert chain([]).nlargest(0).value == []
    assert chain([]).nlargest(1).value == []
    assert chain([1, 3, 2, 4, 3]).nlargest(2).value == [4, 3]
    assert chain([1, 3, 2, 4, 3]).nlargest(3).value == [4, 3, 3]
    assert chain([1, 3, 2, 4, 1]).nlargest(0).value == []


def test_nsmallest():
    assert chain([]).nsmallest(0).value == []
    assert chain([]).nsmallest(1).value == []
    assert chain([1, 3, 2, 4, 1]).nsmallest(2).value == [1, 1]
    assert chain([1, 3, 2, 4, 1]).nsmallest(3).value == [1, 1, 2]
    assert chain([1, 3, 2, 4, 1]).nsmallest(0).value == []
