from pydantic import BaseModel

class Signal(BaseModel):
    id: int
    name: str