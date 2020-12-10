from pydantic import BaseModel

class RoomIn(BaseModel):
    city: str
    isDeluxe: bool
    maxPrice: int