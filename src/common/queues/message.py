from src.common.models import Message


class MessageQueue:

    def announce(self, caller_id: str, reciever_id: str, message: Message):
        raise NotImplementedError("MessageQueue.announce()")

    def consume(self) -> list[Message]:
        raise NotImplementedError("MessageQueue.consume()")
