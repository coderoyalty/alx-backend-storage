#!/usr/bin/env python3
"""
exercise file
"""
import redis
from typing import Union, Optional, Callable
import uuid
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """
    count no. of times a method is called
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        wrapper method
        """
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """
    store the history of inputs and outputs.
    """

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """ Wrapper for decorator functionality """
        key = method.__qualname__
        input = key + ":inputs"
        output = key + ":outputs"
        self._redis.rpush(input, str(args))
        data = method(self, *args, **kwargs)
        self._redis.rpush(output, str(data))
        return data

    return wrapper


def replay(method: Callable) -> None:
    """
    replays the history of a function
    """
    name = method.__qualname__
    cache = redis.Redis()
    calls = cache.get(name).decode()
    print("{} was called {} times:".format(name, calls))
    inputs = cache.lrange(name + ":inputs", 0, -1)
    outputs = cache.lrange(name + ":outputs", 0, -1)
    for i, o in zip(inputs, outputs):
        print("{}(*{}) -> {}".format(name, i.decode(),
                                     o.decode()))


class Cache:
    """cache class"""

    def __init__(self):
        """ initialize cache"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        store data in cache
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str,
            fn: Optional[Callable] = None) -> Union[str, bytes, int, float]:
        """get data from cache"""
        value = self._redis.get(key)
        if fn:
            value = fn(value)
        return value

    def get_int(self, key: str) -> str:
        """automatically parametrize Cache@get_int"""
        value = self.get(key)
        try:
            value = int(value.decode())
        except Exception:
            value = 0
        return value

    def get_str(self, key: str) -> str:
        """automatically parametrize Cache@get_str"""
        value = self.get(key)
        return value.decode()
