#!/usr/bin/env python3
'''
Redis basics
'''
import redis
import uuid
from typing import Union


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
