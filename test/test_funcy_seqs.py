from funcy_chain import Chain


def test_drop():
    assert Chain([]).drop(0).value == []
    assert Chain([]).drop(1).value == []
    assert Chain([1, 2]).drop(0).value == [1, 2]
    assert Chain([1, 2]).drop(1).value == [2]
    assert Chain([1, 2]).drop(2).value == []
    assert Chain([1, 2]).drop(3).value == []


def test_take():
    assert Chain([]).take(0).value == []
    assert Chain([]).take(1).value == []
    assert Chain([1, 2]).take(0).value == []
    assert Chain([1, 2]).take(1).value == [1]
    assert Chain([1, 2]).take(2).value == [1, 2]
    assert Chain([1, 2]).take(3).value == [1, 2]


def test_rest():
    assert Chain([]).rest().value == []
    assert Chain([1]).rest().value == []
    assert Chain([1, 2]).rest().value == [2]


def test_butlast():
    assert Chain([]).butlast().value == []
    assert Chain([1]).butlast().value == []
    assert Chain([1, 2]).butlast().value == [1]


def test_map():
    assert Chain([]).map(lambda x: x.foo).value == []
    assert Chain([]).map(lambda x: x + 1).value == []
    assert Chain([1, 2]).map(lambda x: x + 1).value == [2, 3]


def test_filter():
    assert Chain([]).filter(lambda x: x.foo).value == []
    assert Chain([]).filter(lambda x: x > 1).value == []
    assert Chain([1, 2]).filter(lambda x: x > 1).value == [2]


def test_remove():
    assert Chain([]).remove(lambda x: x).value == []
    assert Chain([0, 1, 2]).remove(lambda x: x != 0).value == [0]
    assert Chain([0, 1, 2]).remove(lambda x: x == 1).value == [0, 2]


def test_keep():
    assert Chain([]).keep().value == []
    assert Chain([]).keep(lambda x: x).value == []
    assert Chain([0, 1, 2]).keep().value == [1, 2]
    assert Chain([0, 1, 2]).keep(lambda x: x - 1).value == [-1, 1]


def test_without():
    assert Chain([]).without(2).value == []
    assert Chain([1, 2, 3]).without().value == [1, 2, 3]
    assert Chain([1, 2, 3]).without(3).value == [1, 2]
    assert Chain([1, 2, 3]).without(2).value == [1, 3]
    assert Chain([1, 2, 3]).without(2, 3).value == [1]
    assert Chain([1, 2, 3]).without(3, 2, 3).value == [1]
    assert Chain([1, 2, 3]).without(1, 2, 3).value == []


def test_concat():
    assert Chain([]).concat().value == []
    assert Chain([[]]).concat().value == []
    assert Chain([[], []]).concat().value == []
    assert Chain([[1, 2]]).concat().value == [1, 2]
    assert Chain([[1, 2], [3]]).concat().value == [1, 2, 3]


def test_flatten():
    assert Chain([]).flatten().value == []
    assert Chain([[]]).flatten().value == []
    assert Chain([[], []]).flatten().value == []
    assert Chain([1, [2], 3]).flatten().value == [1, 2, 3]


def test_mapcat():
    assert Chain([]).mapcat(lambda x: x.foo).value == []
    assert Chain([]).mapcat(lambda x: [x + 1]).value == []
    assert Chain([1, 2]).mapcat(lambda x: [x + 1]).value == [2, 3]
    assert Chain([1, 2]).mapcat(lambda x: [x, -x]).value == [1, -1, 2, -2]


def test_interleave():
    assert Chain([]).interleave().value == []
    assert Chain([[1]]).interleave().value == [1]
    assert Chain([[1, 2]]).interleave().value == [1, 2]
    assert Chain([[1], [2]]).interleave().value == [1, 2]
    assert Chain([[1, 2], [3, 4]]).interleave().value == [1, 3, 2, 4]


def test_interpose():
    assert Chain([]).interpose("X").value == []
    assert Chain(["a"]).interpose("X").value == ["a"]
    assert Chain(["a", "b"]).interpose("X").value == ["a", "X", "b"]
    assert Chain(["a", "b", "c"]).interpose("X").value == ["a", "X", "b", "X", "c"]


def test_takewhile():
    assert Chain([]).takewhile(lambda x: x.foo).value == []
    assert Chain([-1, 0, 1, 2, 3, 4]).takewhile().value == [-1]
    assert Chain([-1, 0, 1, 2, 3, 4]).takewhile(lambda x: x != 3).value == [-1, 0, 1, 2]


def test_dropwhile():
    assert Chain([]).dropwhile(lambda x: x.foo).value == []
    assert Chain([-1, 0, 1, 2, 3, 4]).dropwhile().value == [0, 1, 2, 3, 4]
    assert Chain([-1, 0, 1, 2, 3, 4]).dropwhile(lambda x: x != 3).value == [3, 4]


def test_distinct():
    assert Chain([]).distinct().value == []
    assert Chain([1]).distinct().value == [1]
    assert Chain([1, 2, 1, 3]).distinct().value == [1, 2, 3]


def test_split():
    assert Chain([]).split(lambda x: x.foo).value == ([], [])
    assert Chain([]).split(lambda x: x > 0).value == ([], [])
    assert Chain([-1, 1, 0]).split(lambda x: x > 0).value == ([1], [-1, 0])


def test_split_at():
    assert Chain([]).split_at(0).value == ([], [])
    assert Chain(["a", "b", "c"]).split_at(0).value == ([], ["a", "b", "c"])
    assert Chain(["a", "b", "c"]).split_at(1).value == (["a"], ["b", "c"])
    assert Chain(["a", "b", "c"]).split_at(3).value == (["a", "b", "c"], [])
    assert Chain(["a", "b", "c"]).split_at(4).value == (["a", "b", "c"], [])


def test_split_by():
    assert Chain([]).split_by(lambda x: x.foo).value == ([], [])
    assert Chain([]).split_by(lambda x: x > 0).value == ([], [])
    assert Chain([-1, 1, -1]).split_by(lambda x: x < 0).value == ([-1], [1, -1])


def test_group_by():
    assert Chain([]).group_by(lambda x: x.foo).value == {}
    assert Chain([1, 2, 3]).group_by(lambda x: x % 2).value == {0: [2], 1: [1, 3]}


def test_group_by_keys():
    assert Chain([]).group_by_keys(lambda x: x.foo).value == {}
    assert Chain(["Tom", "Tim"]).group_by_keys(lambda x: (x[0], x[1])).value == {
        "T": ["Tom", "Tim"],
        "o": ["Tom"],
        "i": ["Tim"],
    }


def test_group_values():
    assert Chain([]).group_values().value == {}
    assert Chain([("a", 1), ("b", 2), ("a", 3)]).group_values().value == {"b": [2], "a": [1, 3]}


def test_count_by():
    assert Chain([]).count_by(lambda x: x.foo).value == {}
    assert Chain([1, 2, 3]).count_by(lambda x: x % 2).value == {1: 2, 0: 1}


def test_count_reps():
    assert Chain([]).count_reps().value == {}
    assert Chain([1, 2, 1]).count_reps().value == {1: 2, 2: 1}


def test_partition():
    assert Chain([]).partition(2).value == []
    assert Chain([1]).partition(2).value == []
    assert Chain([1, 2]).partition(2).value == [[1, 2]]
    assert Chain([1, 2, 3]).partition(2).value == [[1, 2]]
    assert Chain([1, 2, 3, 4, 5]).partition(2, 2).value == [[1, 2], [3, 4]]
    assert Chain([1, 2, 3, 4, 5]).partition(2, 3).value == [[1, 2], [4, 5]]
    assert Chain([1, 2, 3, 4, 5, 6, 7]).partition(2, 3).value == [[1, 2], [4, 5]]


def test_chunks():
    assert Chain([]).chunks(2).value == []
    assert Chain([1]).chunks(2).value == [[1]]
    assert Chain([1, 2]).chunks(2).value == [[1, 2]]
    assert Chain([1, 2, 3]).chunks(2).value == [[1, 2], [3]]
    assert Chain([1, 2, 3, 4, 5]).chunks(2, 2).value == [[1, 2], [3, 4], [5]]
    assert Chain([1, 2, 3, 4, 5]).chunks(2, 3).value == [[1, 2], [4, 5]]
    assert Chain([1, 2, 3, 4, 5, 6, 7]).chunks(2, 3).value == [[1, 2], [4, 5], [7]]


def test_partition_by():
    assert Chain([]).partition_by(lambda x: x.foo).value == []
    assert Chain([]).partition_by(lambda x: x % 2).value == []
    assert Chain([1]).partition_by(lambda x: x % 2).value == [[1]]
    assert Chain([1, 2, 4, 3, 5, 2]).partition_by(lambda x: x % 2).value == [
        [1],
        [2, 4],
        [3, 5],
        [2],
    ]


def test_with_prev():
    assert Chain([]).with_prev().value == []
    assert Chain([1]).with_prev().value == [(1, None)]
    assert Chain([1]).with_prev(0).value == [(1, 0)]
    assert Chain([1]).with_prev(fill=0).value == [(1, 0)]
    assert Chain([1, 2, 3]).with_prev().value == [(1, None), (2, 1), (3, 2)]


def test_with_next():
    assert Chain([]).with_next().value == []
    assert Chain([1]).with_next().value == [(1, None)]
    assert Chain([1]).with_next(0).value == [(1, 0)]
    assert Chain([1]).with_next(fill=0).value == [(1, 0)]
    assert Chain([1, 2, 3]).with_next().value == [(1, 2), (2, 3), (3, None)]


def test_pairwise():
    assert Chain([]).pairwise().value == []
    assert Chain([1]).pairwise().value == []
    assert Chain([1, 2, 3]).pairwise().value == [(1, 2), (2, 3)]


def test_accumulate():
    assert Chain([]).accumulate().value == []
    assert Chain([]).accumulate(lambda a, b: a.foo).value == []
    assert Chain([1, 2, 3, 4]).accumulate().value == [1, 3, 6, 10]
    assert Chain([1, 2, 3, 4]).accumulate(lambda acc, x: acc * x).value == [1, 2, 6, 24]


def test_reductions():
    add = lambda a, b: a + b
    mul = lambda a, b: a * b

    assert Chain([]).reductions(lambda a, b: a.foo).value == []
    assert Chain([]).reductions(add).value == []
    assert Chain([1, 2, 3, 4]).reductions(add).value == [1, 3, 6, 10]
    assert Chain([1, 2, 3, 4]).reductions(mul).value == [1, 2, 6, 24]
    assert Chain([1, 2, 3, 4]).reductions(add, acc=-1).value == [0, 2, 5, 9]


def test_sums():
    assert Chain([]).sums().value == []
    assert Chain([1, 2, 3, 4]).sums().value == [1, 3, 6, 10]
    assert Chain([1, 2, 3, 4]).sums(acc=-1).value == [0, 2, 5, 9]
