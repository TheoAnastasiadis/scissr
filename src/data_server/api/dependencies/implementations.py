from mongomock import MongoClient
from pydantic import BaseModel
from redis import StrictRedis
from src.data_server.impl.services.auth.keyclock_auth import KeyCloackAuth
from src.data_server.impl.services.cache.redis_user_cache import RedisUserCache
from src.data_server.impl.services.db.mongo_contacts_db import MongoContactsDB
from src.data_server.impl.services.db.mongo_message_db import MongoMessageDB
from src.common.queues.impl.kafka_message_queue import KafkaMessageQueue
from src.data_server.impl.services.db.mongo_user_db import MongoUserDB
from src.data_server.impl.services.storage.gcloud_storage import (
    GoogleCloudStorage,
)
from common.config import config
from google.cloud.storage import Client as GCSClient
from keycloak import KeycloakOpenID


class Impl(BaseModel):
    # config
    _mongo_uri = config["MONGO_URI"] or ""
    _redis_uri = config["REDIS_URL"] or ""
    _kc_server_uri = config["OIC_SERVER_URL"] or ""
    _kc_server_realm = config["OIC_REALM"] or ""
    _kc_client_id = config["OIC_CLIENT_ID"] or ""
    _kc_client_secret = config["OIC_CLIENT_SERCERT"] or ""
    _kafka_server_url = config["KAFKA_SERVER_URL"] or ""

    # clients
    _mongo_client = MongoClient(_mongo_uri)
    _gcs_client = GCSClient()
    _redis_client = StrictRedis(_redis_uri)
    _kc_oidc = KeycloakOpenID(
        _kc_server_uri, _kc_server_realm, _kc_client_id, _kc_client_secret
    )

    # implementations
    user_db = MongoUserDB(_mongo_client)
    contacts_db = MongoContactsDB(_mongo_client)
    message_db = MongoMessageDB(_mongo_client)
    user_cache = RedisUserCache(_redis_client)
    storage = GoogleCloudStorage(_gcs_client)
    auth_service = KeyCloackAuth(user_db, _kc_oidc)
    message_queue = KafkaMessageQueue(_kafka_server_url)
