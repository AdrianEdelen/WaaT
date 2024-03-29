from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

#TODO: change the avatar url to the an actual blob of the avatar photo

class One_Word_Message(Base):
    __tablename__ = 'one_word_messages'
    id = Column(Integer, primary_key=True)
    content = Column(String)
    discord_timestamp = Column(DateTime)
    user_str = Column(String)
    meta_message = Column(String)
    avatar_url = Column(String)
    createdOn = Column(DateTime)

    user_id = Column(Integer, ForeignKey('users.id'))

    user = relationship("User", back_populates="one_word_messages")

#TODO: implement user storing (this doesn't need to be on any specific channel, just registering users)
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    discord_user_id = Column(String, unique=True)
    display_name = Column(String)
    username = Column(String)
    current_avatar_url = Column(String)
    last_message_sent_id = Column(String)

    one_word_messages = relationship("One_Word_Message", back_populates="user")