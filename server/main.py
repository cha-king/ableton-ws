import asyncio
import logging
from typing import Set

from fastapi import FastAPI, WebSocket, WebSocketDisconnect

from .models import Note


logger = logging.getLogger(__name__)


app = FastAPI()


class ConnectionManager:
    def __init__(self):
        self._websockets: Set[WebSocket] = set()

    async def publish(self, note: Note):
        cos = [
            websocket.send_json(note.dict()) for websocket in self._websockets
        ]
        await asyncio.gather(*cos)

    def subscribe(self, websocket: WebSocket):
        self._websockets.add(websocket)

    def unsubscribe(self, websocket: WebSocket):
        self._websockets.remove(websocket)


manager = ConnectionManager()


@app.post("/publish")
async def publish_note(note: Note):
    await manager.publish(note)


@app.websocket("/ws")
async def get_notes(websocket: WebSocket):
    await websocket.accept()
    logger.info("Client connected")
    manager.subscribe(websocket)
    try:
        while True:
            await websocket.receive_json()
    except WebSocketDisconnect:
        logger.info("Client disconnected")
        manager.unsubscribe(websocket)
