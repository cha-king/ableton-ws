import asyncio
from typing import List
from dataclasses import dataclass, asdict

from fastapi import FastAPI, WebSocket
from pydantic import BaseModel


app = FastAPI()


@dataclass
class Note:
    pitch: int
    velocity: int
    channel: int = 1


class ConnectionManager:
    def __init__(self):
        self._websockets: List[WebSocket] = []

    async def publish(self, note: Note):
        cos = [
            websocket.send_json(asdict(note)) for websocket in self._websockets
        ]
        await asyncio.gather(*cos)

    def subscribe(self, websocket: WebSocket):
        self._websockets.append(websocket)


manager = ConnectionManager()


class NoteRequest(BaseModel):
    pitch: int
    velocity: int
    channel: int = 1


@app.post("/publish")
async def publish_note(note_request: NoteRequest):
    note = Note(note_request.pitch, note_request.velocity)
    await manager.publish(note)


@app.websocket("/ws")
async def get_notes(websocket: WebSocket):
    await websocket.accept()
    manager.subscribe(websocket)
    while True:
        data = await websocket.receive_json()
        note = Note(data['pitch'], data['velocity'])
        await manager.publish(note)
