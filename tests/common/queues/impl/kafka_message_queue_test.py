from uuid import uuid4
from bson import ObjectId
from kafka import KafkaConsumer, KafkaProducer
import pytest
from unittest.mock import MagicMock
from src.common.models.message import Message
from src.common.queues.impl.kafka_message_queue import KafkaMessageQueue

ex_message = Message(
    _id=str(ObjectId()),
    sender=str(uuid4()),
    reciever=str(uuid4()),
    text="Hello!",
)


@pytest.fixture
def mock_kafka_producer():
    producer = MagicMock(spec=KafkaProducer)
    producer.send = MagicMock()
    producer.flush = MagicMock()
    return producer


@pytest.fixture
def mock_kafka_consumer():
    consumer = MagicMock(spec=KafkaConsumer)
    consumer.subscribe = MagicMock()
    return consumer


@pytest.fixture
def kafka_message_queue(mock_kafka_producer, mock_kafka_consumer):
    return KafkaMessageQueue(mock_kafka_producer, mock_kafka_consumer)


def test_announce(kafka_message_queue, mock_kafka_producer):
    kafka_message_queue.announce("Caller1", "Receiver1", ex_message)
    mock_kafka_producer.send.assert_called_once()
    mock_kafka_producer.flush.assert_called_once()


def test_consume(kafka_message_queue, mock_kafka_consumer):
    ex_messages = [
        Message(
            _id=str(ObjectId()),
            sender=str(uuid4()),
            reciever=str(uuid4()),
            text="Hello!",
        ),
        Message(
            _id=str(ObjectId()),
            sender=str(uuid4()),
            reciever=str(uuid4()),
            photo_id=str(ObjectId()),
        ),
    ]
    mock_kafka_consumer.__iter__.return_value = [
        ex_messages[0].model_dump_json(),
        ex_messages[1].model_dump_json(),
    ]
    messages = kafka_message_queue.consume()
    assert len(messages) == 2
    assert messages[0].text == ex_messages[0].text
    assert messages[1].photo_id == ex_messages[1].photo_id
