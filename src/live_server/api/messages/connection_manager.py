from bson import ObjectId
from fastapi import WebSocket

from src.common.models.message import Message


class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[tuple[ObjectId, ObjectId], WebSocket] = (
            {}
        )

    async def register(self, from_id: str, to_id: str, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[(from_id, to_id)] = websocket

    # ~ O(n)
    def delete(self, websocket: WebSocket):
        for key in self.active_connections.keys():
            if self.active_connections[key] == websocket:
                del self.active_connections[key]

    async def notify(self, from_id: str, to_id: str, message: Message):
        if (from_id, to_id) in self.active_connections:
            self.active_connections[(from_id, to_id)].send_text(message)

        if (to_id, from_id) in self.active_connections:
            self.active_connections[(from_id, to_id)].send_text(message)
