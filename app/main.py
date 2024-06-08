from fastapi import Depends, FastAPI, Query
from sqlalchemy.orm import Session
from . import actions, models, models_alvo, schemas, create_data, schemas_alvo, actions_alvo
from .database import SessionLocal, SessionAlvo, engine_fonte, engine_alvo
from datetime import datetime, date

models.Base_fonte.metadata.create_all(bind=engine_fonte)
models_alvo.Base_alvo.metadata.create_all(bind=engine_alvo)
app = FastAPI()

creator = create_data.CreateData(app)
creator.upload_data()

# Dependency
def get_db():
  db = SessionLocal()
  try:
     yield db
  finally:
     db.close()
     
def get_db_alvo():
  db = SessionAlvo()
  try:
     yield db
  finally:
     db.close()

@app.get("/")
def read_root():
  return {"message": "Fastapi written for postgresql database reading and editing"}

@app.get("/all_data/")
def read_data(db: Session = Depends(get_db)):
  data = actions.get_all_data(db)
  return data

@app.get("/data_in_time_range/")
def read_data_range(db: Session = Depends(get_db), start_time: datetime= Query(..., description="Data de início do intervalo"), end_time: datetime= Query(..., description="Data de término do intervalo")):
  data = actions.get_data_in_time_range(db, start_time=start_time, end_time=end_time)
  return data

@app.get("/data_in_day/")
def read_data_day(db: Session = Depends(get_db), day: date= Query(..., description="Dia de busca dos dados")):
  data = actions.get_data_in_day(db, day=day)
  return data

@app.post("/upload_data")
def upload_data(data: schemas.Data, db: Session = Depends(get_db)):   
   return actions.insert_data(db, data)

@app.get("/signals/")
def read_signals(db: Session = Depends(get_db_alvo)):
  data = actions_alvo.get_signals(db)
  return data

@app.get("/alvo/data")
def read_alvo_data(db: Session = Depends(get_db_alvo)):
  data = actions_alvo.get_data(db)
  return data 