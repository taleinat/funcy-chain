import sys
import warnings

import pytest

from funcy_chain import chain


def test_choice():
    assert chain([1, 2, 3]).choice().value in [1, 2, 3]
    with pytest.raises(IndexError):
        chain([]).choice().value


def test_choices():
    assert chain([1, 2, 3]).choices(k=1).value in [[1], [2], [3]]
    assert len(chain([1, 2, 3]).choices(k=4).value) == 4
    assert len(chain([1, 2, 3]).choices([1, 2, 3], k=4).value) == 4
    assert len(chain([1, 2, 3]).choices(weights=[1, 2, 3], k=4).value) == 4
    assert len(chain([1, 2, 3]).choices(cum_weights=[1, 2, 3], k=4).value) == 4
    with pytest.raises(IndexError):
        chain([]).choices(k=1).value


def test_sample():
    assert chain([1, 2, 3]).sample(1).value in [[1], [2], [3]]
    assert len(chain([1, 2, 3]).sample(2).value) == 2
    assert len(chain([1, 2, 3]).sample(3).value) == 3
    with pytest.raises(ValueError):
        chain([]).sample(1).value
    with pytest.raises(ValueError):
        chain([1, 2, 3]).sample(4).value

    if sys.version_info >= (3, 9):
        assert len(chain([1, 2, 3]).sample(8, counts=[3, 3, 3]).value) == 8
        assert set(chain([1, 2, 3]).sample(8, counts=[3, 3, 3]).value) <= {1, 2, 3}
        with pytest.raises(ValueError):
            chain([1, 2, 3]).sample(10, counts=[3, 3, 3]).value


def test_shuffle():
    assert chain([]).shuffle().value == []
    assert chain([1, 2, 3]).shuffle().sort().value == [1, 2, 3]

    # The "random" argument for random.shuffle() is deprecated since Python 3.9.
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", DeprecationWarning)
        assert chain([1, 2, 3]).shuffle(random=lambda: 0.5).sort().value == [1, 2, 3]
