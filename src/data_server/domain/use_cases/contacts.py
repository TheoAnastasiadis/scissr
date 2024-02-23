from src.common.models.contact import Contact
from src.data_server.domain.services.auth.auth_serivce import APICaller
from src.data_server.domain.services.db.contacts import ContactsDB
from pydantic import validate_call


class ContactUseCases:

    contacts_db: ContactsDB

    def __init__(self, contacts_db: ContactsDB):
        self.contacts_db = contacts_db

    @validate_call
    def getContacts(
        self, caller: APICaller, skip: int = 0, limit: int = 20
    ) -> list[Contact]:

        return self.contacts_db.findMany(caller.sub, skip, limit)
