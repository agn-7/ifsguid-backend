from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .config import settings

engine = create_engine(
    settings.SQLALCHEMY_DATABASE_URI.unicode_string(), pool_pre_ping=True
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, future=True, bind=engine)
