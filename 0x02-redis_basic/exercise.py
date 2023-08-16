#!/usr/bin/env python3
"""
exercise file
"""
import redis
from typing import Union
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
