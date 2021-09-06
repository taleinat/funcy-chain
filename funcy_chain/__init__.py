"""Method chaining with funcy functions."""

__version__ = "0.1.1"


from .chain import Chain
from .getter import getter
from .iterchain import IterChain

__all__ = [
    "Chain",
    "IterChain",
    "getter",
]
