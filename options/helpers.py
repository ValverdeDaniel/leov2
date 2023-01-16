import functools
import hashlib
import json
from django.core.cache import cache


def cache_request(timeout=60 * 60):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = f"{func.__name__}_{hashlib.md5(json.dumps(kwargs).encode('utf-8')).hexdigest()}"
            value = cache.get(key)
            if value is None:
                value = func(*args, **kwargs)
                cache.set(key, value, timeout=timeout)
            return value

        return wrapper

    return decorator