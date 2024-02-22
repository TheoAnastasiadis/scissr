from src.common.queues.message import MessageQueue
from src.data_server.domain.services.auth.auth_serivce import APICaller
from src.data_server.domain.services.db.contacts import ContactsDB
from src.data_server.domain.services.db.message import MessageDB
from src.data_server.domain.services.db.user import UserDB
from pydantic import validate_call
from fastapi import HTTPException


class MessageUseCases:

    messages_db: MessageDB
    message_queue: MessageQueue
    user_db: UserDB
    contacts_db: ContactsDB

    def __init__(
        self,
        messages_db: MessageDB,
        message_queue: MessageQueue,
        user_db: UserDB,
        contacts_db: ContactsDB,
    ):
        self.messages_db = messages_db
        self.message_queue = message_queue
        self.user_db = user_db
        self.contacts_db = contacts_db

    @validate_call
    def get_messages(
        self,
        caller: APICaller,
        parties: tuple[str, str],
        skip: int = 0,
        limit: int = 20,
    ):

        if caller.data_id not in parties:
            raise HTTPException(
                status_code=403, detail="You cannot access this resource"
            )

        return self.messages_db.findMany(parties, skip, limit)

    @validate_call
    def send_message(
        self,
        caller: APICaller,
        reciever_id: str,
        text: str = None,
        photo_id: str = None,
    ):
        reciever = self.user_db.findOne(reciever_id)
        if caller.data_id in reciever.blocked:
            raise HTTPException(
                status_code=403, detail="You cannot perform this action"
            )

        if not text and not photo_id:
            raise HTTPException(status_code=400, detail="Invalid Input")

        message = self.messages_db.insert(
            caller.data_id, reciever_id, text, photo_id
        )
        self.contacts_db.update([caller.data_id, reciever_id], text or "photo")
        self.message_queue.announce(caller.data_id, reciever_id, message)
