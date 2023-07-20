#!/usr/bin/env python3
'''
Redis basics
'''
import redis
import uuid
from typing import Union, Optional, Callable
from functools import wraps


def count_calls(methods: Callable) -> Callable:
    ''' count cache class method '''
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        ''' wrapper function for decorators '''
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper

class Cache:
    ''' Cache class '''

    def __init__(self) -> None:
        ''' initializes redis instance '''
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        ''' takes a data argument and returns a string '''
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str,
            fn: Optional[Callable] = None) -> Union[str, bytes, int, float]:
        ''' converts the data back to the desired format '''
        value = self._redis.get(key)
        if fn:
            value = fn(value)
        return value

    def get_str(self, value: bytes) -> str:
        ''' get str from cache '''
        return str(value.decode('utf-8'))

    def get_int(self, value: bytes) -> int:
        ''' get int from the cache '''
        try:
            value = int(value.decode('utf-8'))
        except Exception:
            value = 0
        return value
