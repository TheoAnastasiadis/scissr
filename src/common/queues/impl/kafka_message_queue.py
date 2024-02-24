import json
from kafka import KafkaProducer, KafkaConsumer
from kafka.errors import KafkaError
from typing import List
from src.common.models.message import Message
from src.common.queues.message import MessageQueue


class KafkaMessageQueue(MessageQueue):
    TOPIC = "messages"

    def __init__(self, producer: KafkaProducer, consumer: KafkaConsumer):
        self.producer = producer
        self.consumer = consumer
        self.consumer.subscribe([self.TOPIC])

    def announce(self, caller_id: str, receiver_id: str, message: Message):
        try:
            # Serialize message content before sending
            serialized_message = message.model_dump_json()
            # Produce message to Kafka topic
            self.producer.send(
                self.TOPIC,
                key=caller_id.encode("utf-8"),
                value=serialized_message,
            )
            self.producer.flush()
        except KafkaError as e:
            print(f"Failed to send message: {e}")

    def consume(self) -> List[Message]:
        messages = []
        for msg in self.consumer:
            # Deserialize message content after receiving
            payload = json.loads(msg)
            message = Message(_id = payload.get("id"), **payload)
            messages.append(message)
        return messages
