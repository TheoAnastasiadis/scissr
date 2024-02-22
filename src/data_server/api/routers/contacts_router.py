from fastapi import APIRouter, Depends
from src.data_server.domain.services.auth.auth_serivce import AuthService
from src.data_server.domain.services.db.contacts import ContactsDB
from src.data_server.domain.use_cases.contacts import ContactUseCases


class ContactsRouter:
    tags = ["contacts"]
    contact_use_cases: ContactUseCases
    auth_service: AuthService

    def __init__(
        self,
        contacts_db: ContactsDB,
        auth_service: AuthService,
    ):
        self.contact_use_cases = ContactUseCases(contacts_db)
        self.auth_service = auth_service

    def create_router(self) -> APIRouter:
        router = APIRouter(tags=self.tags)
        get_caller = self.auth_service.get_caller

        @router.get("/contacts")
        def get_contacts(skip=0, limit=20, caller=Depends(get_caller)):
            self.contact_use_cases.getContacts(caller, skip, limit)
