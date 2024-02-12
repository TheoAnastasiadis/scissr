from server.domain.models.message import Message


class MessageDB:

    def insert(
        self,
        sender_id: str,
        reciever_id: str,
        text: str | None,
        photo_id: str | None = None,
    ) -> Message:
        raise NotImplementedError("MessageDB.inser()")

    def findOne(self, id: str) -> Message:
        raise NotImplementedError("MessageDB.findOne()")

    def findMany(
        self,
        sender_id: str,
        reciever_id: str,
        skip=0,
        limit=20,
    ) -> list[Message]:
        raise NotImplementedError("MessageDB.findMany()")
