from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

STRING = os.getenv("DATABASE_URL", "sqlite:///./certificate.db")


engine = create_engine(STRING)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

