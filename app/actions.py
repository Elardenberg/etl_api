from sqlalchemy.orm import Session
from . import models, schemas

def get_data(db: Session, data_id: int):
    return db.query(models.Data).filter(models.Data.id == data_id).first()

def get_all_data(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Data).offset(skip).limit(limit).all()

def insert_data(db: Session, data: schemas.Data):
    db_data = models.Data(
        timestamp = data.timestamp,
        wind_speed = data.wind_speed,
        power = data.power,
        ambient_temperature = data.ambient_temperature
    )
    db.add(db_data)
    db.commit()
    db.refresh(db_data)
    return db_data