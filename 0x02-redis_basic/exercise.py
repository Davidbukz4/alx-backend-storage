#!/usr/bin/env python3
'''
Redis basics
'''
import redis
import uuid
from typing import Union, Optional, Callable


#def count_calls(methods: Callable) -> Callable:

class Cache:
    ''' Cache class '''

    def __init__(self) -> None:
        ''' initializes redis instance '''
        self._redis = redis.Redis()
        self._redis.flushdb()

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
