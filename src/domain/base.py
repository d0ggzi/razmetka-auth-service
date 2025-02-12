from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from src.settings.config import settings

BaseModel = declarative_base(metadata=MetaData())
engine = create_engine(settings.DATABASE_URL_psycopg)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
