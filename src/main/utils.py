'''
Created on Sep 9, 2013

@author: Harold
'''
from functools import wraps

def stringify_args(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        return fn(*map(str, args), **{k: str(v) for k, v in kwargs.items()})

    return wrapper

def memoize(fn):
    class _MemoizingDict(dict):
        def __missing__(self, key):
            v = self[key] = fn(*key)
            return v

    cache = _MemoizingDict()

    def wrapper(*args):
        return cache[args]

    return wrapper