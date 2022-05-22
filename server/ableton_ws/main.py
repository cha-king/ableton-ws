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


@app.websocket("/receive")
async def get_notes(websocket: WebSocket):
    await websocket.accept()
    logger.info("Receive client connected")
    manager.subscribe(websocket)
    try:
        while True:
            await websocket.receive_json()
    except WebSocketDisconnect:
        logger.info("Receive client disconnected")
        manager.unsubscribe(websocket)


@app.websocket("/publish")
async def publish_notes(websocket: WebSocket):
    await websocket.accept()
    logger.info("Publish client connected")
    try:
        while True:
            data = await websocket.receive_json()
            note = Note.parse_obj(data)
            await manager.publish(note)
    except WebSocketDisconnect:
        logger.info("Publish client disconnected")
