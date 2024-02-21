from bson import ObjectId
from src.data_server.impl.services.cache.redis_user_cache import RedisUserCache
import pytest
from src.common.models.user import User
import pygeohash as pgh
from fakeredis import FakeStrictRedis


@pytest.fixture
def redis_user_cache():
    redis_client = FakeStrictRedis()
    return RedisUserCache(redis_client)


def test_cache_set_has_get(redis_user_cache):
    filters = {"only_active": False}
    location = {"latitude": 0, "longitude": 0}
    hash = pgh.encode(**location)
    users = [
        User(
            _id=ObjectId(),
            username="test1",
            email="email1@example.com",
            age=32,
            online_status=False,
            active_mtr=0.5,
            kinky_mtr=0.5,
            location=(0, 0),
        ),
        User(
            _id=ObjectId(),
            username="test2",
            email="email2@example.com",
            age=23,
            online_status=False,
            active_mtr=0.5,
            kinky_mtr=0.5,
            location=(0, 0),
        ),
    ]
    redis_user_cache.cache_set(filters, users, hash)
    assert redis_user_cache.cache_has(filters, hash)
    cached_users = redis_user_cache.cache_get(filters, hash)
    assert len(cached_users) == 2
    assert users == cached_users


def test_cache_get_active_users(redis_user_cache):
    filters = {"only_active": True}
    location = {"latitude": 0, "longitude": 0}
    hash = pgh.encode(**location)
    with pytest.raises(TypeError):
        redis_user_cache.cache_get(filters, hash)


def test_cache_has_active_users(redis_user_cache):
    filters = {"only_active": True}
    location = {"latitude": 0, "longitude": 0}
    hash = pgh.encode(**location)
    with pytest.raises(TypeError):
        redis_user_cache.cache_has(filters, hash)


def test_cache_set_active_users(redis_user_cache):
    filters = {"only_active": True}
    location = {"latitude": 0, "longitude": 0}
    hash = pgh.encode(**location)
    users = [
        User(
            _id=ObjectId(),
            username="test1",
            email="email1@example.com",
            age=32,
            online_status=False,
            active_mtr=0.5,
            kinky_mtr=0.5,
            location=(0, 0),
        ),
        User(
            _id=ObjectId(),
            username="test2",
            email="email2@example.com",
            age=23,
            online_status=False,
            active_mtr=0.5,
            kinky_mtr=0.5,
            location=(0, 0),
        ),
    ]
    with pytest.raises(TypeError):
        redis_user_cache.cache_set(filters, users, hash)
