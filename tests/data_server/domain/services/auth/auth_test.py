import pytest
from src.data_server.domain.services.auth import AuthDB


def test_auth_has_not_implemented():
    with pytest.raises(NotImplementedError) as exc_info:
        AuthDB().user_is_admin("example")
    assert str(exc_info.value) == "AuthDB.user_is_admin()"
