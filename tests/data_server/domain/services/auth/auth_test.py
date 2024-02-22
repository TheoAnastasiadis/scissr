import pytest
from src.data_server.domain.services.auth.auth_serivce import AuthService


def test_auth_not_implemented():
    with pytest.raises(NotImplementedError) as exc_info:
        AuthService().get_caller("")
    assert str(exc_info.value) == "AuthService.get_caller()"
