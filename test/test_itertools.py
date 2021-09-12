def test_starmap(Chain):
    assert Chain([]).starmap(lambda x: x.foo).value == []
    assert Chain([(1, 2), (2, 3), (3, 4)]).starmap(pow).value == [1, 8, 81]


def test_zip_longest(Chain):
    assert Chain([]).zip_longest().value == []
    assert Chain([()]).zip_longest().value == []
    assert Chain([(), ()]).zip_longest().value == []
    assert Chain([(1,), (3,)]).zip_longest().value == [(1, 3)]
    assert Chain([(1, 2)]).zip_longest().value == [(1,), (2,)]
    assert Chain([(1, 2), ()]).zip_longest().value == [(1, None), (2, None)]
    assert Chain([(1, 2), (3,)]).zip_longest().value == [(1, 3), (2, None)]
    assert Chain([(1,), (3, 4)]).zip_longest().value == [(1, 3), (None, 4)]
    assert Chain([(1, 2), (3,)]).zip_longest(fillvalue=0).value == [(1, 3), (2, 0)]
    assert Chain([(1, 2), (3, 4)]).zip_longest().value == [(1, 3), (2, 4)]
    assert Chain([(1, 2), (3, 4)]).zip_longest(fillvalue=0).value == [(1, 3), (2, 4)]
