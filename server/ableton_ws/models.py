from pydantic import BaseModel


class Note(BaseModel):
    pitch: int
    velocity: int
    channel: int = 1
