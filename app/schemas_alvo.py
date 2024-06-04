from pydantic import BaseModel
from datetime import datetime

class Signal(BaseModel):
    id: int
    name: str

class Data(BaseModel):
    id: int
    timestamp: datetime
    signal_id: int
    value: float