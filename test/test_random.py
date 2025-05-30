import sys
import warnings

import pytest


def test_choice(Chain):
    assert Chain([1, 2, 3]).choice().value in [1, 2, 3]
    with pytest.raises(IndexError):
        Chain([]).choice().value


def test_choices(Chain):
    assert Chain([1, 2, 3]).choices(k=1).value in [[1], [2], [3]]
    assert len(Chain([1, 2, 3]).choices(k=4).value) == 4
    assert len(Chain([1, 2, 3]).choices([1, 2, 3], k=4).value) == 4
    assert len(Chain([1, 2, 3]).choices(weights=[1, 2, 3], k=4).value) == 4
    assert len(Chain([1, 2, 3]).choices(cum_weights=[1, 2, 3], k=4).value) == 4
    with pytest.raises(IndexError):
        Chain([]).choices(k=1).value


def test_sample(Chain):
    assert Chain([1, 2, 3]).sample(1).value in [[1], [2], [3]]
    assert len(Chain([1, 2, 3]).sample(2).value) == 2
    assert len(Chain([1, 2, 3]).sample(3).value) == 3
    with pytest.raises(ValueError):
        Chain([]).sample(1).value
    with pytest.raises(ValueError):
        Chain([1, 2, 3]).sample(4).value

    if sys.version_info >= (3, 9):
        assert len(Chain([1, 2, 3]).sample(8, counts=[3, 3, 3]).value) == 8
        assert set(Chain([1, 2, 3]).sample(8, counts=[3, 3, 3]).value) <= {1, 2, 3}
        with pytest.raises(ValueError):
            Chain([1, 2, 3]).sample(10, counts=[3, 3, 3]).value


def test_shuffle(Chain):
    assert Chain([]).shuffle().value == []
    assert Chain([1, 2, 3]).shuffle().sort().value == [1, 2, 3]


# The "random" argument to random.shuffle() was removed in Python 3.11.
@pytest.mark.skipif(sys.version_info >= (3, 11), reason="'random' argument remove in Python 3.11")
def test_shuffle_with_random_argument(Chain):
    # The "random" argument for random.shuffle() is deprecated since Python 3.9.
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", DeprecationWarning)
        assert Chain([1, 2, 3]).shuffle(random=lambda: 0.5).sort().value == [1, 2, 3]
