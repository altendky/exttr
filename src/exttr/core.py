import collections
import functools
import itertools
import uuid

import attr

import exttr._utility


attr_ib_keywords = exttr._utility.get_parameter_names(attr.ib)

metadata_name = 'exttr'

class UnknownKeywordError(Exception):
    pass


class KeywordCollisionError(Exception):
    pass


class AttrsCollisionError(Exception):
    pass


def get_all(cls, attribute):
    fields = attr.fields(cls)
    field = getattr(fields, attribute)
    metadata = field.metadata[metadata_name]

    return metadata


def get(cls, attribute, extra):
    return get_all(cls=cls, attribute=attribute)[extra]


@attr.s(frozen=True)
class Keyword(object):
    name = attr.ib()
    uuid = attr.ib(
        default=None,
        converter=lambda x: None if x is None else uuid.UUID(x),
    )


@attr.s
class Plugin(object):
    keywords = attr.ib(factory=list, converter=list)

    def register_keywords(self, *keywords):
        for keyword in keywords:
            self.keywords.append(keyword)


@attr.s
class Registry(object):
    plugins = attr.ib(factory=list, converter=list)

    def register_plugins(self, *plugins):
        for plugin in plugins:
            for keyword in plugin.keywords:
                if keyword.name in attr_ib_keywords:
                    raise AttrsCollisionError(keyword)

                for other_keyword in self.keywords():
                    name_collision = (
                        (keyword == other_keyword)
                        and (keyword.uuid is None)
                    )

                    uuid_collision = (
                        (keyword.uuid == other_keyword.uuid)
                        and (keyword.name != other_keyword.name)
                    )

                    uuid_mismatch = (
                        (keyword.uuid != other_keyword.uuid)
                        and (keyword.name == other_keyword.name)
                    )

                    if name_collision or uuid_collision or uuid_mismatch:
                        raise KeywordCollisionError(
                            'Existing: {}, New: {}'.format(
                                other_keyword,
                                keyword,
                            ),
                        )

            self.plugins.append(plugin)

    def register_keywords(self, *keywords):
        plugin = Plugin()
        plugin.register_keywords(*keywords)

        self.register_plugins(plugin)

    @functools.wraps(attr.ib)
    def create_attribute(self, *args, **kwargs):
        extra_names = set(kwargs.keys()) - set(attr_ib_keywords)

        unknown_names = (
            extra_names - {keyword.name for keyword in self.keywords()}
        )

        if len(unknown_names) != 0:
            raise UnknownKeywordError(
                ', '.join(repr(name) for name in unknown_names),
            )

        metadata = kwargs.setdefault('metadata', {})
        exttrs_metadata = metadata.setdefault(metadata_name, {})

        extras = {
            k: v
            for k, v in kwargs.items() 
            if k in extra_names
        }

        exttrs_metadata.update(extras)

        basics = collections.OrderedDict(
            (k, v)
            for k, v in kwargs.items() 
            if k in attr_ib_keywords
        )

        return attr.ib(*args, **basics)

    def keywords(self):
        return set(itertools.chain.from_iterable(
            (
                keyword
                for keyword in plugin.keywords
            )
            for plugin in self.plugins
        ))
