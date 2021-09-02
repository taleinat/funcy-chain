"""Method chaining with funcy functions."""

__version__ = "0.1.0"


from .chain import FuncyChain

__all__ = [
    "chain",
]


def chain(value):
    return FuncyChain(value)