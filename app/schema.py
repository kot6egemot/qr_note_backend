from pydantic import BaseModel, Field


class QrNote(BaseModel):
    id: str
    qr: str
    title: str = Field(min_length=1)
    description: str
