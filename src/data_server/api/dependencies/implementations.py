from mongomock import MongoClient
from pydantic import BaseModel
from redis import StrictRedis
from src.data_server.impl.services.auth.keyclock_auth import KeyCloackAuth
from src.data_server.impl.services.cache.redis_user_cache import RedisUserCache
from src.data_server.impl.services.db.mongo_contacts_db import MongoContactsDB
from src.data_server.impl.services.db.mongo_message_db import MongoMessageDB

from src.data_server.impl.services.db.mongo_user_db import MongoUserDB
from src.data_server.impl.services.storage.gcloud_storage import (
    GoogleCloudStorage,
)
from google.cloud.storage import Client as GCSClient


class Impl(BaseModel):
    # clients
    _mongo_client = MongoClient(...)
    _gcs_client = GCSClient(...)
    _redis_client = StrictRedis(...)
    # implementations
    user_db = MongoUserDB(_mongo_client)
    contacts_db = MongoContactsDB(_mongo_client)
    message_db = MongoMessageDB(_mongo_client)
    user_cache = RedisUserCache(_redis_client)
    storage = GoogleCloudStorage(_gcs_client)
    auth_service = KeyCloackAuth(user_db)
