import functools
import sys
from heapq import nlargest, nsmallest
from itertools import islice
from random import choice, choices, sample, shuffle

import funcy
from funcy.funcmakers import make_func

from .chain_base import ChainBase
from .utils import UNSET

MIN_MAX_KEY_ACCEPTS_NONE = sys.version_info >= (3, 8)


class IterChain(ChainBase):

    ## builtins

    def enumerate(self, start=0):
        return IterChain(enumerate(self._value, start=start))

    def max(self, key=None):
        return IterChain(max(self._value, key=make_func(key, builtin=MIN_MAX_KEY_ACCEPTS_NONE)))

    def min(self, key=None):
        return IterChain(min(self._value, key=make_func(key, builtin=MIN_MAX_KEY_ACCEPTS_NONE)))

    def reduce(self, f, *initializer):
        return IterChain(functools.reduce(make_func(f, builtin=True), self._value, *initializer))

    def reverse(self):
        try:
            value = reversed(self._value)
        except TypeError:
            value = reversed(list(self._value))
        return IterChain(value)

    def slice(self, *args):
        return IterChain(islice(self._value, *args))

    def sort(self, key=None, reverse=False):
        return IterChain(sorted(self._value, key=make_func(key, builtin=True), reverse=reverse))

    def sum(self, start=UNSET):
        args = (start,) if start is not UNSET else ()
        return IterChain(sum(self._value, *args))

    ## heapq

    def nlargest(self, n, key=None):
        return IterChain(nlargest(n, self._value, key=make_func(key, builtin=True)))

    def nsmallest(self, n, key=None):
        return IterChain(nsmallest(n, self._value, key=make_func(key, builtin=True)))

    ## random

    def choice(self):
        return IterChain(choice(self._value))

    def choices(self, weights=None, *, cum_weights=None, k=1):
        return IterChain(choices(self._value, weights, cum_weights=cum_weights, k=k))

    if sys.version_info < (3, 9):

        def sample(self, k):
            return IterChain(sample(self._value, k))

    else:

        def sample(self, k, *, counts=None):
            return IterChain(sample(self._value, k, counts=counts))

    def shuffle(self, random=None):
        kwargs = dict(random=random) if random is not None else {}
        value = list(self._value)
        shuffle(value, **kwargs)
        return IterChain(value)

    ## dicts

    def items(self):
        return IterChain(self._value.items())

    def values(self):
        return IterChain(self._value.values())

    def keys(self):
        return IterChain(self._value.keys())

    def update(self, *args, **kwargs):
        value = self._value.copy()
        value.update(*args, **kwargs)
        return IterChain(value)

    ## funcy.colls

    def join(self):
        return IterChain(funcy.join(self._value))

    merge = join

    def join_with(self, f):
        return IterChain(funcy.join_with(f, self._value))

    merge_with = join_with

    def walk(self, f):
        return IterChain(funcy.walk(f, self._value))

    def walk_keys(self, f):
        return IterChain(funcy.walk_keys(f, self._value))

    def walk_values(self, f):
        return IterChain(funcy.walk_values(f, self._value))

    def select(self, f):
        return IterChain(funcy.select(f, self._value))

    def select_keys(self, f):
        return IterChain(funcy.select_keys(f, self._value))

    def select_values(self, f):
        return IterChain(funcy.select_values(f, self._value))

    def compact(self):
        return IterChain(funcy.compact(self._value))

    def flip(self):
        return IterChain(funcy.flip(self._value))

    def project(self, keys):
        return IterChain(funcy.project(self._value, keys))

    def omit(self, keys):
        return IterChain(funcy.omit(self._value, keys))

    def zip_values(self):
        # funcy.zip_values() raises a TypeError for empty collections, but that's annoying.
        if len(self._value) == 0:
            return IterChain([])
        return IterChain(funcy.zip_values(*self._value))

    def zip_dicts(self):
        # funcy.zip_dicts() raises a TypeError for empty collections, but that's annoying.
        if len(self._value) == 0:
            return IterChain([])
        return IterChain(funcy.zip_dicts(*self._value))

    def where(self, **cond):
        return IterChain(funcy.where(self._value, **cond))

    def pluck(self, key):
        return IterChain(funcy.pluck(key, self._value))

    def pluck_attr(self, attr):
        return IterChain(funcy.pluck_attr(attr, self._value))

    def invoke(self, name, *args, **kwargs):
        return IterChain(funcy.invoke(self._value, name, *args, **kwargs))

    ## funcy.seqs

    def drop(self, n):
        return IterChain(funcy.drop(n, self._value))

    def take(self, n):
        return IterChain(funcy.take(n, self._value))

    def rest(self):
        return IterChain(funcy.rest(self._value))

    def butlast(self):
        return IterChain(funcy.butlast(self._value))

    def map(self, f):
        return IterChain(funcy.map(f, self._value))

    def filter(self, predicate):
        return IterChain(funcy.filter(predicate, self._value))

    def remove(self, pred):
        return IterChain(funcy.remove(pred, self._value))

    def keep(self, f=UNSET):
        if f is UNSET:
            return IterChain(funcy.keep(self._value))
        else:
            return IterChain(funcy.keep(f, self._value))

    def without(self, *items):
        return IterChain(funcy.without(self._value, *items))

    def concat(self):
        return IterChain(funcy.cat(self._value))

    def flatten(self, follow=UNSET):
        kwargs = dict(follow=follow) if follow is not UNSET else {}
        return IterChain(funcy.flatten(self._value, **kwargs))

    def mapcat(self, f):
        return IterChain(funcy.mapcat(f, self._value))

    def interleave(self):
        return IterChain(funcy.interleave(*self._value))

    def interpose(self, sep):
        return IterChain(funcy.interpose(sep, self._value))

    def takewhile(self, pred=UNSET):
        if pred is UNSET:
            return IterChain(funcy.takewhile(self._value))
        else:
            return IterChain(funcy.takewhile(pred, self._value))

    def dropwhile(self, pred=UNSET):
        if pred is UNSET:
            return IterChain(funcy.dropwhile(self._value))
        else:
            return IterChain(funcy.dropwhile(pred, self._value))

    def distinct(self, key=UNSET):
        kwargs = dict(key=key) if key is not UNSET else {}
        return IterChain(funcy.distinct(self._value, **kwargs))

    def split(self, pred):
        return IterChain(funcy.split(pred, self._value))

    def split_at(self, n):
        return IterChain(funcy.split_at(n, self._value))

    def split_by(self, pred):
        return IterChain(funcy.split_by(pred, self._value))

    def group_by(self, f):
        return IterChain(funcy.group_by(f, self._value))

    def group_by_keys(self, get_keys):
        return IterChain(funcy.group_by_keys(get_keys, self._value))

    def group_values(self):
        return IterChain(funcy.group_values(self._value))

    def count_by(self, f):
        return IterChain(funcy.count_by(f, self._value))

    def count_reps(self):
        return IterChain(funcy.count_reps(self._value))

    def partition(self, n, step=UNSET):
        if step is UNSET:
            return IterChain(funcy.partition(n, self._value))
        else:
            return IterChain(funcy.partition(n, step, self._value))

    def chunks(self, n, step=UNSET):
        if step is UNSET:
            return IterChain(funcy.chunks(n, self._value))
        else:
            return IterChain(funcy.chunks(n, step, self._value))

    def partition_by(self, f):
        return IterChain(funcy.partition_by(f, self._value))

    def with_prev(self, fill=None):
        return IterChain(funcy.with_prev(self._value, fill=fill))

    def with_next(self, fill=None):
        return IterChain(funcy.with_next(self._value, fill=fill))

    def pairwise(self):
        return IterChain(funcy.pairwise(self._value))

    def accumulate(self, func=UNSET):
        kwargs = dict(func=func) if func is not UNSET else {}
        return IterChain(funcy.accumulate(self._value, **kwargs))

    def reductions(self, f, acc=UNSET):
        kwargs = dict(acc=acc) if acc is not UNSET else {}
        return IterChain(funcy.reductions(f, self._value, **kwargs))

    def sums(self, acc=UNSET):
        kwargs = dict(acc=acc) if acc is not UNSET else {}
        return IterChain(funcy.sums(self._value, **kwargs))
