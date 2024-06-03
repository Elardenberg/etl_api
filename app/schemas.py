from pydantic import BaseModel
from datetime import datetime

class Data(BaseModel):
    id: int
    timestamp: datetime
    wind_speed: float
    power: float
    ambient_temperature: float