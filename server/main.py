import asyncio
import logging
from typing import List

from fastapi import FastAPI, WebSocket

from .models import Note


logger = logging.getLogger(__name__)


app = FastAPI()


class ConnectionManager:
    def __init__(self):
        self._websockets: List[WebSocket] = []

    async def publish(self, note: Note):
        cos = [
            websocket.send_json(note.dict()) for websocket in self._websockets
        ]
        await asyncio.gather(*cos)

    def subscribe(self, websocket: WebSocket):
        self._websockets.append(websocket)


manager = ConnectionManager()


@app.post("/publish")
async def publish_note(note: Note):
    await manager.publish(note)


@app.websocket("/ws")
async def get_notes(websocket: WebSocket):
    await websocket.accept()
    manager.subscribe(websocket)
    while True:
        data = await websocket.receive_json()
        note = Note.parse_obj(data)
        await manager.publish(note)
