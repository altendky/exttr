import attr
import pytest

import exttr


@pytest.fixture(scope='function', autouse=True)
def temporary_global_registry():
    original = exttr.registry

    exttr.registry = exttr.Registry()
    yield
    exttr.registry = original


def test_register_keyword():
    keyword = exttr.Keyword(name='blue')
    exttr.register_keywords(keyword)

    @attr.s
    class C:
        a = exttr.ib(blue=27)

    assert exttr.get(C, 'a') == {'blue': 27}


def test_check_keyword():
    keyword = exttr.Keyword(name='blue')
    exttr.register_keywords(keyword)

    @attr.s
    class C:
        a = exttr.ib(blue=27)

    assert exttr.get(C, 'a', 'blue') == 27


def test_not_registered_keyword():
    with pytest.raises(exttr.UnknownKeywordError):
        exttr.ib(blue=27)


def test_keyword_collision_both_none():
    first_keyword = exttr.Keyword(name='mine')
    exttr.register_keywords(first_keyword)

    second_keyword = exttr.Keyword(name='mine')

    with pytest.raises(exttr.KeywordCollisionError):
        exttr.register_keywords(second_keyword)


def test_keyword_collision_none_and_uuid():
    first_keyword = exttr.Keyword(name='mine')
    exttr.register_keywords(first_keyword)

    second_keyword = exttr.Keyword(
        name='mine',
        uuid='cdfed248-158d-493a-9a62-7a6ea927a3fa',
    )

    with pytest.raises(exttr.KeywordCollisionError):
        exttr.register_keywords(second_keyword)


def test_keyword_collision_uuid_and_none():
    first_keyword = exttr.Keyword(
        name='mine',
        uuid='9ff4c722-e541-4e78-a23b-6209a6ea83dd',
    )
    exttr.register_keywords(first_keyword)

    second_keyword = exttr.Keyword(name='mine')

    with pytest.raises(exttr.KeywordCollisionError):
        exttr.register_keywords(second_keyword)


def test_keyword_collision_different_uuid():
    first_keyword = exttr.Keyword(
        name='mine',
        uuid='43e059b3-42dc-49f8-a762-946b4ca6efec',
    )
    exttr.register_keywords(first_keyword)

    second_keyword = exttr.Keyword(
        name='mine',
        uuid='518b04a7-5875-4986-9012-e5786ae528dd',
    )

    with pytest.raises(exttr.KeywordCollisionError):
        exttr.register_keywords(second_keyword)


def test_multiple_keyword_matched_uuid():
    first_keyword = exttr.Keyword(
        name='mine',
        uuid='66d2d925-c7b7-4132-9652-92b92cb57c5f',
    )
    exttr.register_keywords(first_keyword)

    second_keyword = exttr.Keyword(
        name='mine',
        uuid='66d2d925-c7b7-4132-9652-92b92cb57c5f',
    )

    exttr.register_keywords(second_keyword)


def test_attrs_keyword_collision():
    # just a selection of long-existing attr.ib() parameters
    for name in ('default', 'repr', 'metadata'): 
        keyword = exttr.Keyword(name=name)

        with pytest.raises(exttr.AttrsCollisionError):
            exttr.register_keywords(keyword)
