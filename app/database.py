from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_FONTE_URL = "postgresql+psycopg2://postgres:postgres@localhost:5432/fonte"
SQLALCHEMY_ALVO_URL = "postgresql+psycopg2://postgres:postgres@localhost:5432/alvo"


engine_fonte = create_engine(SQLALCHEMY_FONTE_URL)
engine_alvo = create_engine(SQLALCHEMY_ALVO_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine_fonte)
SessionAlvo = sessionmaker(autocommit=False, autoflush=False, bind=engine_alvo)

Base_fonte = declarative_base()
Base_alvo = declarative_base()