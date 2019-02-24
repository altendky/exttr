from ._version import get_versions
__version__ = get_versions()['version']
del get_versions

from exttr.core import (
    AttrsCollisionError,
    get,
    Keyword,
    KeywordCollisionError,
    Plugin,
    Registry,
    UnknownKeywordError,
)

registry = Registry()

def ib(*args, **kwargs):
    return registry.create_attribute(*args, **kwargs)

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
