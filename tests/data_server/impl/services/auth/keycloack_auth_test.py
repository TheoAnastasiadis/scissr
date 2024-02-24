from fastapi import HTTPException
from src.data_server.domain.services.db.user import UserDB
from src.data_server.impl.services.auth.keyclock_auth import KeyCloackAuth
from keycloak import KeycloakOpenID
import pytest
from unittest.mock import MagicMock


@pytest.fixture
def user_db():
    return MagicMock(spec=UserDB)


@pytest.fixture
def keycloak_client():
    return MagicMock(sepc=KeycloakOpenID)


@pytest.fixture
def keycloak_auth(
    user_db,
    keycloak_client,
):
    return KeyCloackAuth(
        user_db,
        keycloak_client,
    )


def test_get_payload_success(keycloak_auth, keycloak_client):
    token = "dummy_token"
    keycloak_client.decode_token.return_value = {
        "sub": "123",
        "email": "test@example.com",
        "preferred_username": "test_user",
    }
    payload = keycloak_auth._get_payload(token)
    assert payload == {
        "sub": "123",
        "email": "test@example.com",
        "preferred_username": "test_user",
    }


def test_get_payload_failure(keycloak_auth, keycloak_client):
    token = "dummy_token"
    keycloak_client.decode_token.side_effect = Exception(
        "Token decoding failed"
    )
    with pytest.raises(HTTPException):
        keycloak_auth._get_payload(token)


def test_get_caller(keycloak_auth, keycloak_client):
    token = "dummy_token"
    keycloak_client.decode_token.return_value = {
        "sub": "123",
        "email": "test@example.com",
        "preferred_username": "test_user",
    }
    caller = keycloak_auth.get_caller(token)
    assert caller.sub == "123"
    assert caller.email == "test@example.com"
    assert caller.p_username == "test_user"


def test_get_caller_failure(keycloak_auth, keycloak_client):
    token = "dummy_token"
    keycloak_client.decode_token.side_effect = Exception(
        "Token decoding failed"
    )
    with pytest.raises(HTTPException):
        keycloak_auth.get_caller(token)
