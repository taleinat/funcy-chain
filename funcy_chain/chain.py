import functools
import sys
from heapq import nlargest, nsmallest
from random import choice, choices, sample, shuffle

import funcy
from funcy.funcmakers import make_func

from .chain_base import ChainBase
from .utils import UNSET

MIN_MAX_KEY_ACCEPTS_NONE = sys.version_info >= (3, 8)


class FuncyChain(ChainBase):

    ## builtins

    def enumerate(self, start=0):
        return FuncyChain(list(enumerate(self._value, start=start)))

    def max(self, key=None):
        return FuncyChain(max(self._value, key=make_func(key, builtin=MIN_MAX_KEY_ACCEPTS_NONE)))

    def min(self, key=None):
        return FuncyChain(min(self._value, key=make_func(key, builtin=MIN_MAX_KEY_ACCEPTS_NONE)))

    def sort(self, key=None, reverse=False):
        return FuncyChain(sorted(self._value, key=make_func(key, builtin=True), reverse=reverse))

    def reduce(self, f, *initializer):
        return FuncyChain(functools.reduce(make_func(f, builtin=True), self._value, *initializer))

    def reverse(self):
        return FuncyChain(list(reversed(self._value)))

    ## heapq

    def nlargest(self, n, key=None):
        return FuncyChain(nlargest(n, self._value, key=key))

    def nsmallest(self, n, key=None):
        return FuncyChain(nsmallest(n, self._value, key=key))

    ## random

    def choice(self):
        return FuncyChain(choice(self._value))

    def choices(self, weights=None, *, cum_weights=None, k=1):
        return FuncyChain(choices(self._value, weights, cum_weights=cum_weights, k=k))

    if sys.version_info < (3, 9):

        def sample(self, k):
            return FuncyChain(sample(self._value, k))

    else:

        def sample(self, k, *, counts=None):
            return FuncyChain(sample(self._value, k, counts=counts))

    def shuffle(self, random=None):
        kwargs = dict(random=random) if random is not None else {}
        value = list(self._value)
        shuffle(value, **kwargs)
        return FuncyChain(value)

    ## dicts

    def items(self):
        return FuncyChain(list(self._value.items()))

    def values(self):
        return FuncyChain(list(self._value.values()))

    def keys(self):
        return FuncyChain(list(self._value.keys()))

    def update(self, *args, **kwargs):
        value = self._value.copy()
        value.update(*args, **kwargs)
        return FuncyChain(value)

    ## funcy.colls

    def join(self):
        return FuncyChain(funcy.join(self._value))

    merge = join

    def join_with(self, f):
        return FuncyChain(funcy.join_with(f, self._value))

    merge_with = join_with

    def walk(self, f):
        return FuncyChain(funcy.walk(f, self._value))

    def walk_keys(self, f):
        return FuncyChain(funcy.walk_keys(f, self._value))

    def walk_values(self, f):
        return FuncyChain(funcy.walk_values(f, self._value))

    def select(self, f):
        return FuncyChain(funcy.select(f, self._value))

    def select_keys(self, f):
        return FuncyChain(funcy.select_keys(f, self._value))

    def select_values(self, f):
        return FuncyChain(funcy.select_values(f, self._value))

    def compact(self):
        return FuncyChain(funcy.compact(self._value))

    def flip(self):
        return FuncyChain(funcy.flip(self._value))

    def project(self, keys):
        return FuncyChain(funcy.project(self._value, keys))

    def omit(self, keys):
        return FuncyChain(funcy.omit(self._value, keys))

    def zip_values(self):
        # funcy.zip_values() raises a TypeError for empty collections, but that's annoying.
        if len(self._value) == 0:
            return FuncyChain([])
        return FuncyChain(list(funcy.zip_values(*self._value)))

    def zip_dicts(self):
        # funcy.zip_dicts() raises a TypeError for empty collections, but that's annoying.
        if len(self._value) == 0:
            return FuncyChain([])
        return FuncyChain(list(funcy.zip_dicts(*self._value)))

    def where(self, **cond):
        return FuncyChain(list(funcy.lwhere(self._value, **cond)))

    def pluck(self, key):
        return FuncyChain(list(funcy.lpluck(key, self._value)))

    def pluck_attr(self, attr):
        return FuncyChain(list(funcy.lpluck_attr(attr, self._value)))

    def invoke(self, name, *args, **kwargs):
        return FuncyChain(list(funcy.linvoke(self._value, name, *args, **kwargs)))

    ## funcy.seqs

    def drop(self, n):
        return FuncyChain(list(funcy.drop(n, self._value)))

    def take(self, n):
        return FuncyChain(funcy.take(n, self._value))

    def rest(self):
        return FuncyChain(list(funcy.rest(self._value)))

    def butlast(self):
        return FuncyChain(list(funcy.butlast(self._value)))

    def map(self, f):
        return FuncyChain(funcy.lmap(f, self._value))

    def filter(self, predicate):
        return FuncyChain(funcy.lfilter(predicate, self._value))

    def remove(self, pred):
        return FuncyChain(funcy.lremove(pred, self._value))

    def keep(self, f=UNSET):
        if f is UNSET:
            return FuncyChain(funcy.lkeep(self._value))
        else:
            return FuncyChain(funcy.lkeep(f, self._value))

    def without(self, *items):
        return FuncyChain(funcy.lwithout(self._value, *items))

    def concat(self):
        return FuncyChain(funcy.lcat(self._value))

    def flatten(self, follow=UNSET):
        kwargs = dict(follow=follow) if follow is not UNSET else {}
        return FuncyChain(funcy.lflatten(self._value, **kwargs))

    def mapcat(self, f):
        return FuncyChain(funcy.lmapcat(f, self._value))

    def interleave(self):
        return FuncyChain(list(funcy.interleave(*self._value)))

    def interpose(self, sep):
        return FuncyChain(list(funcy.interpose(sep, self._value)))

    def takewhile(self, pred=UNSET):
        if pred is UNSET:
            return FuncyChain(list(funcy.takewhile(self._value)))
        else:
            return FuncyChain(list(funcy.takewhile(pred, self._value)))

    def dropwhile(self, pred=UNSET):
        if pred is UNSET:
            return FuncyChain(list(funcy.dropwhile(self._value)))
        else:
            return FuncyChain(list(funcy.dropwhile(pred, self._value)))

    def distinct(self, key=UNSET):
        kwargs = dict(key=key) if key is not UNSET else {}
        return FuncyChain(funcy.ldistinct(self._value, **kwargs))

    def split(self, pred):
        return FuncyChain(funcy.lsplit(pred, self._value))

    def split_at(self, n):
        return FuncyChain(funcy.lsplit_at(n, self._value))

    def split_by(self, pred):
        return FuncyChain(funcy.lsplit_by(pred, self._value))

    def group_by(self, f):
        return FuncyChain(funcy.group_by(f, self._value))

    def group_by_keys(self, get_keys):
        return FuncyChain(funcy.group_by_keys(get_keys, self._value))

    def group_values(self):
        return FuncyChain(funcy.group_values(self._value))

    def count_by(self, f):
        return FuncyChain(funcy.count_by(f, self._value))

    def count_reps(self):
        return FuncyChain(funcy.count_reps(self._value))

    def partition(self, n, step=UNSET):
        if step is UNSET:
            return FuncyChain(funcy.lpartition(n, self._value))
        else:
            return FuncyChain(funcy.lpartition(n, step, self._value))

    def chunks(self, n, step=UNSET):
        if step is UNSET:
            return FuncyChain(funcy.lchunks(n, self._value))
        else:
            return FuncyChain(funcy.lchunks(n, step, self._value))

    def partition_by(self, f):
        return FuncyChain(funcy.lpartition_by(f, self._value))

    def with_prev(self, fill=None):
        return FuncyChain(list(funcy.with_prev(self._value, fill=fill)))

    def with_next(self, fill=None):
        return FuncyChain(list(funcy.with_next(self._value, fill=fill)))

    def pairwise(self):
        return FuncyChain(list(funcy.pairwise(self._value)))

    def accumulate(self, func=UNSET):
        kwargs = dict(func=func) if func is not UNSET else {}
        return FuncyChain(list(funcy.accumulate(self._value, **kwargs)))

    def reductions(self, f, acc=UNSET):
        kwargs = dict(acc=acc) if acc is not UNSET else {}
        return FuncyChain(funcy.lreductions(f, self._value, **kwargs))

    def sums(self, acc=UNSET):
        kwargs = dict(acc=acc) if acc is not UNSET else {}
        return FuncyChain(funcy.lsums(self._value, **kwargs))
