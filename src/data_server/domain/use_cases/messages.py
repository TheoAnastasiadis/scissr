from src.common.models.message import Message
from src.common.models.user import User
from src.common.queues.message import MessageQueue
from data_server.domain.services.db.auth import AuthDB
from data_server.domain.services.db.contacts import ContactsDB
from data_server.domain.services.db.message import MessageDB
from data_server.domain.services.db.user import UserDB
from pydantic import validate_call
from fastapi import HTTPException


class MessageUseCases:

    auth_db: AuthDB
    messages_db: MessageDB
    message_queue: MessageQueue
    user_db: UserDB
    contacts_db: ContactsDB

    def __init__(
        self,
        auth_db: AuthDB,
        messages_db: MessageDB,
        message_queue: MessageQueue,
        user_db: UserDB,
        contacts_db: ContactsDB,
    ):
        self.auth_db = auth_db
        self.messages_db = messages_db
        self.message_queue = message_queue
        self.user_db = user_db
        self.contacts_db = contacts_db

    @validate_call
    def get_persisted_messages(
        self,
        caller: User,
        parties: tuple[str, str],
        skip: int = 0,
        limit: int = 20,
    ):
        is_admin = self.auth_db.user_is_admin()

        if not is_admin and caller.id not in parties:
            raise HTTPException(
                status_code=403, detail="You cannot access this resource"
            )

        return self.messages_db.findMany(parties, skip, limit)

    @validate_call
    def get_live_messages(self) -> list[Message]:
        return self.message_queue.consume()

    @validate_call
    def send_message(
        self,
        caller: User,
        reciever_id: str,
        text: str = None,
        photo_id: str = None,
    ):
        # admin cannot do this
        reciever = self.user_db.findOne(reciever_id)
        if reciever.id in caller.blocked or caller.id in reciever.blocked:
            raise HTTPException(
                status_code=403, detail="You cannot perform this action"
            )

        if not text and not photo_id:
            raise HTTPException(status_code=400, detail="Invalid Input")

        message = self.messages_db.insert(
            caller.id, reciever_id, text, photo_id
        )
        self.contacts_db.update([caller.id, reciever_id], text or "photo")
        self.message_queue.announce(caller.id, reciever_id, message)
