from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.types import Float

from .database import Base_alvo

class Signal(Base_alvo):
    __tablename__ = "signal"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

class Data(Base_alvo):
    __tablename__ = "data"
    id = Column(Integer, primary_key=True, index=True)
    signal_id = Column(Integer, ForeignKey('signal.id'))
    timestamp = Column(Float)
    value = Column(Float)