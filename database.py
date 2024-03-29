# # database.py
# from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker
# import logging

# class Database:
#     Base = declarative_base()

#     def __init__(self, database_url) -> None:
#         self.logger = logging.getLogger(__name__)
#         self.database_url = database_url
#         self.engine = None
#         self.SessionLocal = None

#     def init_database(self):
#         try:
#             self.logger.debug("Creating DB Engine")
#             self.engine = create_engine(self.database_url, echo=True, future=True)
#             self.logger.debug("Creating Local DB Session")
#             self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
#             result = True
#         except Exception as e:
#             self.logger.exception(e)
#             result = False
#         finally:
#             return result
        
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
import logging

#TODO: Get rid of this global
Base = declarative_base()

class Database:
    _instance = None

    def __init__(self, database_url):
        self.logger = logging.getLogger(__name__)
        self.database_url = database_url
        self._engine = None
        self._SessionLocal = None
        self.Base = declarative_base()

    @property
    def engine(self):
        if self._engine is None:
            self.logger.debug("Creating DB Engine - Lazy")
            self._engine = create_engine(self.database_url, echo=True, future=True)
        return self._engine

    @property
    def SessionLocal(self):
        if self._SessionLocal is None:
            self.logger.debug("Creating DB Local Session - Lazy")
            self._SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        return self._SessionLocal

    @classmethod
    def get_instance(cls, database_url=None):
        if cls._instance is None:
            if database_url is None:
                raise ValueError("Database URL is required for the first initialization.")
            cls._instance = cls(database_url)
        return cls._instance

# Usage example
def get_db_session():
    database_url = os.getenv("DATABASE_URL")  # Ensure this is called after environment variables are loaded
    db_instance = Database.get_instance(database_url)
    return db_instance.SessionLocal()
