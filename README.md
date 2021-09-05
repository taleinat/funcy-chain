# funcy-chain

Method chaining with [funcy](https://github.com/Suor/funcy).

```python3
>>> from funcy_chain import Chain
>>> (
...     Chain([1, 2, 3, 7, 6, 5, 4])
...     .without(3)
...     .filter(lambda x: x > 2)
...     .remove(lambda x: x > 6)
...     .sort(reverse=True)
... ).value
[6, 5, 4]
```

```python3
users = [
  { 'user': 'barney',  'age': 36 },
  { 'user': 'fred',    'age': 40 },
  { 'user': 'pebbles', 'age': 1 }
]

youngest = (
    Chain(users)
    .sort(key="age")
    
```

## Why?

[funcy](https://github.com/Suor/funcy) is great, but doesn't support method chaining.
[pydash](https://github.com/dgilland/pydash) is similar to funcy and does support chaining, but it
is more complex and its chains are harder to debug. funcy-chain enables method chaining with
built-in, stdlib and funcy functions, in a way that is simple and straightforward.
