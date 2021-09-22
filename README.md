# funcy-chain

Simple Python data processing using method-chaining style and the funcy library.

```pycon
>>> users = [
...   { 'first_name': 'barney',  'age': 36 },
...   { 'first_name': 'fred',    'age': 40 },
...   { 'first_name': 'pebbles', 'age': 1 }
... ]
>>> (Chain(users)
...     .sort(key=itemgetter("age"))
...     .map(itemgetter("first_name"))
...     .thru(lambda names: names + ["wilma"])
...     .map(str.capitalize)
... ).value
['Pebbles', 'Barney', 'Fred', 'Wilma']
```


# Why?

* Method chaining can make some multi-stage data processing easier to read and write.
* [Funcy](https://github.com/Suor/funcy) is great, but doesn't support method chaining.
* Other method-chaining implementations have too much "magic", are overly complex, and support too many
  ways of doing one thing. (see: [pydash](https://pydash.readthedocs.io/en/latest/chaining.html),
  [fluentpy](https://fluentpy.readthedocs.io/en/latest/fluentpy/fluentpy.html))
* Being simple and straightforward is a great boon, making it easier to reason about code, debug,
  etc.


# Key Features

* Useful out of the box, supporting built-in, stdlib and funcy functions (see [below](#supported-methods)).
* Easy to compose with additional utilities (see `Chain.thru()`).
* Both "immediate" (list-based) and "lazy" (iterator-based) computations supported,
  via parallel `Chain` and `IterChain` classes.

```pycon
>>> from funcy_chain import Chain
>>> (Chain([1, 2, 3, 7, 6, 5, 4])
...     .without(3)
...     .filter(lambda x: x > 2)
...     .remove(lambda x: x > 6)
...     .sort(reverse=True)
... ).value
[6, 5, 4]
```


# Supported Methods

## built-in

* [enumerate](https://docs.python.org/3/library/functions.html#enumerate)
* [max](https://docs.python.org/3/library/functions.html#max)
* [min](https://docs.python.org/3/library/functions.html#min)
* [reduce](https://docs.python.org/3/library/functions.html#reduce)
* [reverse](https://docs.python.org/3/library/functions.html#reverse)
* [slice](https://docs.python.org/3/library/itertools.html#itertools.islice)
* [sort](https://docs.python.org/3/library/functions.html#sort)
* [sum](https://docs.python.org/3/library/functions.html#sum)
* [zip](https://docs.python.org/3/library/functions.html#zip)
* [dict.items](https://docs.python.org/3/library/stdtypes.html#dict.items)
* [dict.keys](https://docs.python.org/3/library/stdtypes.html#dict.keys)
* [dict.values](https://docs.python.org/3/library/stdtypes.html#dict.values)
* [dict.update](https://docs.python.org/3/library/stdtypes.html#dict.update)

Note: funcy's `map` and `filter` are used rather than the built-ins.

## stdlib

* [itertools.starmap](https://docs.python.org/3/library/itertools.html#itertools.starmap)
* [itertools.zip_longest](https://docs.python.org/3/library/itertools.html#itertools.zip_longest)
* [heapq.nlargest](https://docs.python.org/3/library/heapq.html#heapq.nlargest)
* [heapq.nsmallest](https://docs.python.org/3/library/heapq.html#heapq.nsmallest)
* [random.choice](https://docs.python.org/3/library/random.html#random.choice)
* [random.choices](https://docs.python.org/3/library/random.html#random.choices)
* [random.sample](https://docs.python.org/3/library/random.html#random.sample)
* [random.shuffle](https://docs.python.org/3/library/random.html#random.shuffle)

## funcy

The following is a sub-set of the funcy
[cheat sheet](https://funcy.readthedocs.io/en/stable/cheatsheet.html) including only functions
supported as methods on `Chain` and `IterChain` objects.

### Sequences

<table>
<tr><td>Slice</td><td><a href="https://funcy.readthedocs.io/en/stable/seqs.html#drop">drop</a> <a href="https://funcy.readthedocs.io/en/stable/seqs.html#take">take</a> <a href="https://funcy.readthedocs.io/en/stable/seqs.html#rest">rest</a> <a href="https://funcy.readthedocs.io/en/stable/seqs.html#butlast">butlast</a> <a href="https://funcy.readthedocs.io/en/stable/seqs.html#takewhile">takewhile</a> <a href="https://funcy.readthedocs.io/en/stable/seqs.html#dropwhile">dropwhile</a> <a href="https://funcy.readthedocs.io/en/stable/seqs.html#split_at">split_at</a> <a href="https://funcy.readthedocs.io/en/stable/seqs.html#split_by">split_by</a></td></tr>
<tr><td>Transform</td><td><a href="https://funcy.readthedocs.io/en/stable/seqs.html#map">map</a> <a href="https://funcy.readthedocs.io/en/stable/seqs.html#mapcat">mapcat</a> <a href="https://funcy.readthedocs.io/en/stable/seqs.html#keep">keep</a> <a href="https://funcy.readthedocs.io/en/stable/colls.html#pluck">pluck</a> <a href="https://funcy.readthedocs.io/en/stable/colls.html#pluck_attr">pluck_attr</a> <a href="https://funcy.readthedocs.io/en/stable/colls.html#invoke">invoke</a></td></tr>
<tr><td>Filter</td><td><a href="https://funcy.readthedocs.io/en/stable/seqs.html#filter">filter</a> <a href="https://funcy.readthedocs.io/en/stable/seqs.html#remove">remove</a> <a href="https://funcy.readthedocs.io/en/stable/seqs.html#keep">keep</a> <a href="https://funcy.readthedocs.io/en/stable/seqs.html#distinct">distinct</a> <a href="https://funcy.readthedocs.io/en/stable/colls.html#where">where</a> <a href="https://funcy.readthedocs.io/en/stable/seqs.html#without">without</a></td></tr>
<tr><td>Join</td><td><a href="https://funcy.readthedocs.io/en/stable/seqs.html#concat">concat</a> <a href="https://funcy.readthedocs.io/en/stable/seqs.html#flatten">flatten</a> <a href="https://funcy.readthedocs.io/en/stable/seqs.html#mapcat">mapcat</a> <a href="https://funcy.readthedocs.io/en/stable/seqs.html#interleave">interleave</a> <a href="https://funcy.readthedocs.io/en/stable/seqs.html#interpose">interpose</a></td></tr>
<tr><td>Partition</td><td><a href="https://funcy.readthedocs.io/en/stable/seqs.html#chunks">chunks</a> <a href="https://funcy.readthedocs.io/en/stable/seqs.html#partition">partition</a> <a href="https://funcy.readthedocs.io/en/stable/seqs.html#partition_by">partition_by</a> <a href="https://funcy.readthedocs.io/en/stable/seqs.html#split_at">split_at</a> <a href="https://funcy.readthedocs.io/en/stable/seqs.html#split_by">split_by</a></td></tr>
<tr><td>Group</td><td><a href="https://funcy.readthedocs.io/en/stable/seqs.html#split">split</a> <a href="https://funcy.readthedocs.io/en/stable/seqs.html#count_by">count_by</a> <a href="https://funcy.readthedocs.io/en/stable/seqs.html#count_reps">count_reps</a> <a href="https://funcy.readthedocs.io/en/stable/seqs.html#group_by">group_by</a> <a href="https://funcy.readthedocs.io/en/stable/seqs.html#group_by_keys">group_by_keys</a> <a href="https://funcy.readthedocs.io/en/stable/seqs.html#group_values">group_values</a></td></tr>
<tr><td>Aggregate</td><td><a href="https://funcy.readthedocs.io/en/stable/seqs.html#with_prev">with_prev</a> <a href="https://funcy.readthedocs.io/en/stable/seqs.html#with_next">with_next</a> <a href="https://docs.python.org/3/library/itertools.html#itertools.accumulate">accumulate</a> <a href="https://funcy.readthedocs.io/en/stable/seqs.html#reductions">reductions</a> <a href="https://funcy.readthedocs.io/en/stable/seqs.html#sums">sums</a></td></tr>
<tr><td>Iterate</td><td><a href="https://funcy.readthedocs.io/en/stable/seqs.html#pairwise">pairwise</a> <a href="https://funcy.readthedocs.io/en/stable/seqs.html#with_prev">with_prev</a> <a href="https://funcy.readthedocs.io/en/stable/seqs.html#with_next">with_next</a> <a href="https://funcy.readthedocs.io/en/stable/colls.html#zip_values">zip_values</a> <a href="https://funcy.readthedocs.io/en/stable/colls.html#zip_dicts">zip_dicts</a></td></tr>
</table>

### Collections

<table>
<tr><td>Join</td><td><a href="https://funcy.readthedocs.io/en/stable/colls.html#join">join</a> <a href="https://funcy.readthedocs.io/en/stable/colls.html#join_with">join_with</a></td></tr>
<tr><td>Transform</td><td><a href="https://funcy.readthedocs.io/en/stable/colls.html#walk">walk</a> <a href="https://funcy.readthedocs.io/en/stable/colls.html#walk_keys">walk_keys</a> <a href="https://funcy.readthedocs.io/en/stable/colls.html#walk_values">walk_values</a></td></tr>
<tr><td>Filter</td><td><a href="https://funcy.readthedocs.io/en/stable/colls.html#select">select</a> <a href="https://funcy.readthedocs.io/en/stable/colls.html#select_keys">select_keys</a> <a href="https://funcy.readthedocs.io/en/stable/colls.html#select_values">select_values</a> <a href="https://funcy.readthedocs.io/en/stable/colls.html#compact">compact</a></td></tr>
<tr><td>Dicts</td><td><a href="https://funcy.readthedocs.io/en/stable/colls.html#flip">flip</a> <a href="https://funcy.readthedocs.io/en/stable/colls.html#pluck">pluck</a> <a href="https://funcy.readthedocs.io/en/stable/colls.html#wher <a href="https://funcy.readthedocs.io/en/stable/colls.html#project">where</a> [omit](https://funcy.readthedocs.io/en/stable/colls.html#omit">project</a> <a href="https://funcy.readthedocs.io/en/stable/colls.html#zip_values">zip_values</a> <a href="https://funcy.readthedocs.io/en/stable/colls.html#zip_dicts">zip_dicts</a></td></tr>
</table>
