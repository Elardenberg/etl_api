from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from . import actions, models, models_alvo, schemas, create_data
from .database import SessionLocal, engine_fonte, engine_alvo

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

@app.get("/")
def root():
    return {"message": "Hello World!"}

# @app.post("/data/", response_model=schemas.User)
# def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
#   db_user = actions.get_user_by_email(db, email=user.email)
#   if db_user:
#     raise HTTPException(status_code=400, detail="Email already registered")
#   return actions.create_user(db=db, user=user)

@app.get("/all_data/", response_model=list[schemas.Data])
def read_data(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
  data = actions.get_all_data(db, skip=skip, limit=limit)
  return data

@app.post("/upload_data", response_model=list[schemas.Data])
def upload_data(data: schemas.Data, db: Session = Depends(get_db)):   
   return actions.insert_data(db, data)
   