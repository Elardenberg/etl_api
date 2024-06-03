from sqlalchemy import DateTime, Column, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.types import Float

from .database import Base_fonte

class Data(Base_fonte):
    __tablename__ = "data"
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime)
    wind_speed = Column(Float)
    power = Column(Float)
    ambient_temperature = Column(Float)