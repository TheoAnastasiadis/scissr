from unittest.mock import Mock
from src.data_server.domain.services.auth.auth_serivce import APICaller
from src.data_server.domain.services.db.contacts import ContactsDB
from src.data_server.domain.use_cases.contacts import ContactUseCases
import pytest

ex_caller = APICaller(data_id="example", email="", roles=[])


@pytest.fixture
def contacts_use_cases():
    mock_contacts_db = Mock(spec=ContactsDB)
    return ContactUseCases(mock_contacts_db)


def test_get_contacts_admin(contacts_use_cases):
    contacts_db = contacts_use_cases.contacts_db

    contacts_use_cases.getContacts(ex_caller, 0, 20)

    contacts_db.findMany.assert_called_once_with(ex_caller.data_id, 0, 20)
