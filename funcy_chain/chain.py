import sys
from functools import reduce
from heapq import nlargest, nsmallest
from itertools import starmap, zip_longest
from random import choice, choices, sample, shuffle

import funcy
from funcy.funcmakers import make_func, make_pred

from .chain_base import ChainBase
from .utils import UNSET

MIN_MAX_KEY_ACCEPTS_NONE = sys.version_info >= (3, 8)


class Chain(ChainBase):

    ## builtins

    def enumerate(self, start=0):
        return Chain(list(enumerate(self._value, start=start)))

    def max(self, key=None):
        return Chain(max(self._value, key=make_func(key, builtin=MIN_MAX_KEY_ACCEPTS_NONE)))

    def min(self, key=None):
        return Chain(min(self._value, key=make_func(key, builtin=MIN_MAX_KEY_ACCEPTS_NONE)))

    def reduce(self, f, *initializer):
        return Chain(reduce(make_func(f, builtin=True), self._value, *initializer))

    def reverse(self):
        return Chain(list(reversed(self._value)))

    def slice(self, *args):
        return Chain(self._value.__getitem__(slice(*args)))

    def sort(self, key=None, reverse=False):
        return Chain(sorted(self._value, key=make_func(key, builtin=True), reverse=reverse))

    def sum(self, start=UNSET):
        args = (start,) if start is not UNSET else ()
        return Chain(sum(self._value, *args))

    if sys.version_info < (3, 10):

        def zip(self):
            return Chain(list(zip(*self._value)))

    else:

        def zip(self, strict=UNSET):
            kwargs = dict(strict=strict) if strict is not UNSET else {}
            return Chain(list(zip(*self._value, **kwargs)))

    ## itertools

    def starmap(self, f):
        return Chain(list(starmap(f, self._value)))

    def zip_longest(self, fillvalue=None):
        return Chain(list(zip_longest(*self._value, fillvalue=fillvalue)))

    ## heapq

    def nlargest(self, n, key=None):
        return Chain(nlargest(n, self._value, key=make_func(key, builtin=True)))

    def nsmallest(self, n, key=None):
        return Chain(nsmallest(n, self._value, key=make_func(key, builtin=True)))

    ## random

    def choice(self):
        return Chain(choice(self._value))

    def choices(self, weights=None, *, cum_weights=None, k=1):
        return Chain(choices(self._value, weights, cum_weights=cum_weights, k=k))

    if sys.version_info < (3, 9):

        def sample(self, k):
            return Chain(sample(self._value, k))

    else:

        def sample(self, k, *, counts=None):
            return Chain(sample(self._value, k, counts=counts))

    def shuffle(self, random=None):
        kwargs = dict(random=random) if random is not None else {}
        value = list(self._value)
        shuffle(value, **kwargs)
        return Chain(value)

    ## dicts

    def items(self):
        return Chain(list(self._value.items()))

    def values(self):
        return Chain(list(self._value.values()))

    def keys(self):
        return Chain(list(self._value.keys()))

    def update(self, *args, **kwargs):
        value = self._value.copy()
        value.update(*args, **kwargs)
        return Chain(value)

    ## funcy.colls

    def join(self):
        return Chain(funcy.join(self._value))

    merge = join

    def join_with(self, f):
        return Chain(funcy.join_with(make_func(f), self._value))

    merge_with = join_with

    def walk(self, f):
        return Chain(funcy.walk(make_func(f), self._value))

    def walk_keys(self, f):
        return Chain(funcy.walk_keys(make_func(f), self._value))

    def walk_values(self, f):
        return Chain(funcy.walk_values(make_func(f), self._value))

    def select(self, f):
        return Chain(funcy.select(make_func(f), self._value))

    def select_keys(self, f):
        return Chain(funcy.select_keys(make_func(f), self._value))

    def select_values(self, f):
        return Chain(funcy.select_values(make_func(f), self._value))

    def compact(self):
        return Chain(funcy.compact(self._value))

    def flip(self):
        return Chain(funcy.flip(self._value))

    def project(self, keys):
        return Chain(funcy.project(self._value, keys))

    def omit(self, keys):
        return Chain(funcy.omit(self._value, keys))

    def zip_values(self):
        # funcy.zip_values() raises a TypeError for empty collections, but that's annoying.
        if len(self._value) == 0:
            return Chain([])
        return Chain(list(funcy.zip_values(*self._value)))

    def zip_dicts(self):
        # funcy.zip_dicts() raises a TypeError for empty collections, but that's annoying.
        if len(self._value) == 0:
            return Chain([])
        return Chain(list(funcy.zip_dicts(*self._value)))

    def where(self, **cond):
        return Chain(list(funcy.lwhere(self._value, **cond)))

    def pluck(self, key):
        return Chain(list(funcy.lpluck(key, self._value)))

    def pluck_attr(self, attr):
        return Chain(list(funcy.lpluck_attr(attr, self._value)))

    def invoke(self, name, *args, **kwargs):
        return Chain(list(funcy.linvoke(self._value, name, *args, **kwargs)))

    ## funcy.seqs

    def drop(self, n):
        return Chain(list(funcy.drop(n, self._value)))

    def take(self, n):
        return Chain(funcy.take(n, self._value))

    def rest(self):
        return Chain(list(funcy.rest(self._value)))

    def butlast(self):
        return Chain(list(funcy.butlast(self._value)))

    def map(self, f):
        return Chain(funcy.lmap(make_func(f), self._value))

    def filter(self, predicate):
        return Chain(funcy.lfilter(make_pred(predicate), self._value))

    def remove(self, predicate):
        return Chain(funcy.lremove(make_pred(predicate), self._value))

    def keep(self, f=UNSET):
        if f is UNSET:
            return Chain(funcy.lkeep(self._value))
        else:
            return Chain(funcy.lkeep(make_func(f, test=True), self._value))

    def without(self, *items):
        return Chain(funcy.lwithout(self._value, *items))

    def concat(self):
        return Chain(funcy.lcat(self._value))

    def flatten(self, follow=UNSET):
        kwargs = dict(follow=follow) if follow is not UNSET else {}
        return Chain(funcy.lflatten(self._value, **kwargs))

    def mapcat(self, f):
        return Chain(funcy.lmapcat(make_func(f), self._value))

    def interleave(self):
        return Chain(list(funcy.interleave(*self._value)))

    def interpose(self, sep):
        return Chain(list(funcy.interpose(sep, self._value)))

    def takewhile(self, pred=UNSET):
        if pred is UNSET:
            return Chain(list(funcy.takewhile(self._value)))
        else:
            return Chain(list(funcy.takewhile(pred, self._value)))

    def dropwhile(self, pred=UNSET):
        if pred is UNSET:
            return Chain(list(funcy.dropwhile(self._value)))
        else:
            return Chain(list(funcy.dropwhile(pred, self._value)))

    def distinct(self, key=UNSET):
        kwargs = dict(key=key) if key is not UNSET else {}
        return Chain(funcy.ldistinct(self._value, **kwargs))

    def split(self, pred):
        return Chain(funcy.lsplit(pred, self._value))

    def split_at(self, n):
        return Chain(funcy.lsplit_at(n, self._value))

    def split_by(self, pred):
        return Chain(funcy.lsplit_by(pred, self._value))

    def group_by(self, f):
        return Chain(funcy.group_by(make_func(f), self._value))

    def group_by_keys(self, get_keys):
        return Chain(funcy.group_by_keys(make_func(get_keys), self._value))

    def group_values(self):
        return Chain(funcy.group_values(self._value))

    def count_by(self, f):
        return Chain(funcy.count_by(make_func(f), self._value))

    def count_reps(self):
        return Chain(funcy.count_reps(self._value))

    def partition(self, n, step=UNSET):
        if step is UNSET:
            return Chain(funcy.lpartition(n, self._value))
        else:
            return Chain(funcy.lpartition(n, step, self._value))

    def chunks(self, n, step=UNSET):
        if step is UNSET:
            return Chain(funcy.lchunks(n, self._value))
        else:
            return Chain(funcy.lchunks(n, step, self._value))

    def partition_by(self, f):
        return Chain(funcy.lpartition_by(make_func(f), self._value))

    def with_prev(self, fill=None):
        return Chain(list(funcy.with_prev(self._value, fill=fill)))

    def with_next(self, fill=None):
        return Chain(list(funcy.with_next(self._value, fill=fill)))

    def pairwise(self):
        return Chain(list(funcy.pairwise(self._value)))

    def accumulate(self, func=UNSET):
        kwargs = dict(func=make_func(func)) if func is not UNSET else {}
        return Chain(list(funcy.accumulate(self._value, **kwargs)))

    def reductions(self, f, acc=UNSET):
        kwargs = dict(acc=acc) if acc is not UNSET else {}
        return Chain(funcy.lreductions(make_func(f), self._value, **kwargs))

    def sums(self, acc=UNSET):
        kwargs = dict(acc=acc) if acc is not UNSET else {}
        return Chain(funcy.lsums(self._value, **kwargs))
