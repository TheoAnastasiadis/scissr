from src.data_server.domain.services.cache.user_cache import UserCache
import pytest


def test_cache_has_not_implemented():
    cache = UserCache()
    with pytest.raises(NotImplementedError) as exc_info:
        cache.cache_has({}, "")
    assert str(exc_info.value) == "UserCache.has()"


def test_cache_get_not_implemented():
    cache = UserCache()
    with pytest.raises(NotImplementedError) as exc_info:
        cache.cache_get({}, "")
    assert str(exc_info.value) == "UserCache.get()"


def test_cache_set_not_implemented():
    cache = UserCache()
    with pytest.raises(NotImplementedError) as exc_info:
        cache.cache_set({}, [], "")
    assert str(exc_info.value) == "UserCache.set()"
