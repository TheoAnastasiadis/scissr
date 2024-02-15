from src.common.models.contact import Contact
from src.common.models.user import User
from data_server.domain.services.db.auth import AuthDB
from data_server.domain.services.db.contacts import ContactsDB
from fastapi import HTTPException


class ContactUsesCases:

    contacts_db: ContactsDB
    auth_db: AuthDB

    def __init__(self, contacts_db: ContactsDB, auth_db: AuthDB):
        self.contacts_db = ContactsDB
        self.auth_db = auth_db

    def getContacts(
        self, caller: User, user_id: str, skip: int = 0, limit: int = 0
    ) -> list[Contact]:
        is_admin = self.auth_db.user_is_admin(caller.id)

        if not is_admin and caller.id != user_id:
            raise HTTPException(
                status_code=403, detail="You cannot access this resource"
            )

        return self.contacts_db.findMany(user_id, skip, limit)
