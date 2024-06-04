from sqlalchemy.orm import Session
from . import models_alvo

def get_signals(db: Session):
    return db.query(models_alvo.Signal).all()