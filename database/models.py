from .base import Base
from sqlalchemy import Column, Integer, String, DateTime


class WaatWord(Base):
    __tablename__ = 'waat_words'

    id = Column(Integer, primary_key=True, autoincrement=True)
    word = Column(String)
    timestamp = Column(DateTime(timezone=True))
    user = Column(String)
    createdOn = Column(DateTime(timezone=True))
    meta_message = Column(String)
    avatar_url = Column(String)

    def __repr__(self):
        return f"<waat_word(word={self.word}, timestamp={self.timestamp}, user={self.user})"