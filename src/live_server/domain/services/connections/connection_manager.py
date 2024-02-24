from fastapi import WebSocket
from src.common.models.message import Message


class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[str, WebSocket] = {}

    async def connect(self, caller_uuid: str, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[caller_uuid] = websocket

    def disconnect(self, websocket: WebSocket):
        for key in self.active_connections:
            if self.active_connections[key] == websocket:
                del self.active_connections[key]

    async def publish_message(self, reciever_uuid: str, message: Message):
        if reciever_uuid in self.active_connections:
            await self.active_connections[reciever_uuid].send_json(message)
