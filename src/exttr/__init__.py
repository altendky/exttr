from ._version import get_versions

__version__ = get_versions()['version']
del get_versions

import functools

from exttr.core import (
    AttrsCollisionError,
    get,
    get_all,
    Keyword,
    KeywordCollisionError,
    Plugin,
    Registry,
    UnknownKeywordError,
)

registry = Registry()


@functools.wraps(registry.create_attribute)
def ib(*args, **kwargs):
    return registry.create_attribute(*args, **kwargs)


@functools.wraps(registry.register_keywords)
def register_keywords(*args, **kwargs):
    return registry.register_keywords(*args, **kwargs)


__all__ = [
    'AttrsCollisionError',
    'ib',
    'get',
    'Keyword',
    'KeywordCollisionError',
    'Plugin',
    'register_keywords',
    'Registry',
    'UnknownKeywordError',
]
