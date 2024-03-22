from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Word(Base):
    __tablename__ = 'Words'
    id = Column(Integer, primary_key=True)
    content = Column(String)
    discord_timestamp = Column(DateTime)
    user_id = Column(Integer, ForeignKey('users.id'))

    user = relationship("User", back_populates="words")

class User(Base):
    __tablename__ = 'Users'
    id = Column(Integer, primary_key=True)
    accent_color = Column(String)
    avatar = Column()
    name = Column(String)
    email = Column(String)