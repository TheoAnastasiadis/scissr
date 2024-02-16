from src.common.models.contact import Contact
from src.common.models.user import User
from src.data_server.domain.services.auth import AuthDB
from src.data_server.domain.services.db.contacts import ContactsDB
from fastapi import HTTPException
from pydantic import validate_call


class ContactUseCases:

    contacts_db: ContactsDB
    auth_db: AuthDB

    def __init__(self, contacts_db: ContactsDB, auth_db: AuthDB):
        self.contacts_db = contacts_db
        self.auth_db = auth_db

    @validate_call
    def getContacts(
        self, caller: User, user_id: str, skip: int = 0, limit: int = 20
    ) -> list[Contact]:
        is_admin = self.auth_db.user_is_admin(caller.id)

        if not is_admin and caller.id != user_id:
            raise HTTPException(
                status_code=403, detail="You cannot access this resource"
            )

        return self.contacts_db.findMany(user_id, skip, limit)
