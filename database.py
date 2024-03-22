# database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import logging


Base = declarative_base()
engine = None
SessionLocal = None

def init_database(DATABASE_URL):
    logger = logging.getLogger(__name__)
    logger.debug(f"Initializing Database with SQL Alchemy")
    global engine, SessionLocal
    logger.debug("Creating DB Engine")
    engine = create_engine(DATABASE_URL, echo=True, future=True)
    logger.debug("Creating Local DB Session")
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
