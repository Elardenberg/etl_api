from sqlalchemy.orm import Session
from sqlalchemy import func, Date
from . import models, schemas
import datetime

def get_data_in_time_range(db: Session, start_time: datetime.datetime, end_time: datetime.datetime):
    return db.query(models.Data).filter(models.Data.timestamp >= start_time).filter(models.Data.timestamp <= end_time).all()

def get_data_in_day(db: Session, day: datetime.date):
    return db.query(models.Data).filter(func.cast(models.Data.timestamp, Date) == day).all()

def get_all_data(db: Session):
    return db.query(models.Data).all()

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