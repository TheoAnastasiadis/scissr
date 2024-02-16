from datetime import datetime
from bson import ObjectId
from src.common.models.message import Message
from src.common.queues.message import MessageQueue
import pytest


def test_announce_not_implemented():
    queue = MessageQueue()
    with pytest.raises(NotImplementedError) as exc_info:
        queue.announce(
            "user1",
            "user2",
            Message(
                _id=str(ObjectId()),
                sender="user1",
                reciever="user2",
                text="example",
                time_stamp=datetime.now(),
            ),
        )
    assert str(exc_info.value) == "MessageQueue.announce()"


def test_consume_not_implemented():
    queue = MessageQueue()
    with pytest.raises(NotImplementedError) as exc_info:
        queue.consume()
    assert str(exc_info.value) == "MessageQueue.consume()"
