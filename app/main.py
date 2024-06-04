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


@app.get("/all_data/", response_model=list[schemas.Data])
def read_data(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
  data = actions.get_all_data(db, skip=skip, limit=limit)
  return data

@app.get("/data_in_time_range/", response_model=list[schemas.Data])
def read_data_range(db: Session = Depends(get_db), start_time: datetime= Query(..., description="Data de início do intervalo"), end_time: datetime= Query(..., description="Data de término do intervalo")):
  data = actions.get_data_in_time_range(db, start_time=start_time, end_time=end_time)
  return data

@app.get("/data_in_day/", response_model=list[schemas.Data])
def read_data_day(db: Session = Depends(get_db), day: date= Query(..., description="Dia de busca dos dados")):
  data = actions.get_data_in_day(db, day=day)
  return data

@app.post("/upload_data", response_model=list[schemas.Data])
def upload_data(data: schemas.Data, db: Session = Depends(get_db)):   
   return actions.insert_data(db, data)

@app.get("/signals/", response_model=list[schemas_alvo.Signal])
def read_signals(db: Session = Depends(get_db_alvo)):
  data = actions_alvo.get_signals(db)
  return data   