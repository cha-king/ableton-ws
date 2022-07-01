import logging
from uuid import UUID

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect

from .models import Note


logger = logging.getLogger(__name__)


app = FastAPI()


clients: dict[UUID, WebSocket] = {}


@app.websocket("/receive/{client_id}")
async def get_notes(websocket: WebSocket, client_id: UUID):
    await websocket.accept()
    logger.info("Receive client connected")
    clients[client_id] = websocket
    try:
        while True:
            await websocket.receive_json()
    except WebSocketDisconnect:
        logger.info("Receive client disconnected")
        del clients[client_id]


@app.websocket("/publish/{client_id}")
async def publish_notes(websocket: WebSocket, client_id: UUID):
    if client_id not in clients:
        raise HTTPException(status_code=404, detail="Client not found")

    await websocket.accept()
    logger.info("Publish client connected")
    try:
        while True:
            data = await websocket.receive_json()
            note = Note.parse_obj(data)
            ws = clients.get(client_id)
            # Check if client has disconnected
            if ws is None:
                await websocket.close(code=1001, reason="Client disconnected")
        
            await ws.send_json(note.dict())

    except WebSocketDisconnect:
        logger.info("Publish client disconnected")
