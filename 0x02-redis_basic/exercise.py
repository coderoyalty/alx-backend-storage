#!/usr/bin/env python3
"""
exercise file
"""
import redis
from typing import Union, Optional, Callable
import uuid


class Cache:
    """cache class"""

    def __init__(self):
        """ initialize cache"""
        self._redis = redis.Redis()
        self._redis.flushdb()

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
