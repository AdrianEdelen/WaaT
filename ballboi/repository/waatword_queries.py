from sqlalchemy.orm import Session
from database.models import WaatWord
from database.session import get_session
from typing import List
from datetime import datetime, timedelta, timezone

def get_most_recent_waat_word() -> WaatWord:
    with get_session() as session:
        return session.query(WaatWord).order_by(WaatWord.id.desc()).first()

def get_all_waat_words() -> List[WaatWord]:
    with get_session() as session:
        words = session.query(WaatWord).order_by(WaatWord.id.asc()).all()
        return words

def get_waat_word_by_id(id) -> WaatWord:
    with get_session() as session:
        try:
            word = session.query(WaatWord).filter(WaatWord.id == id).one()
            return word
        except Exception as e:
            session.rollback()
            print(f"error retrieving waat word by id: {e}")

def add_new_word(word, user, timestamp, meta_message, avatar_url) -> int:
    with get_session() as session:
        try:
            new_word = WaatWord(word=word, user=user, timestamp=timestamp, meta_message=meta_message, avatar_url=avatar_url, createdOn=datetime.now(timezone.utc))
            session.add(new_word)
            session.commit()
            print(f"added: {new_word}")
            return new_word.id
        except sqlalchemy as e:
            session.rollback()
            print("Error adding new word:", str(e))
        finally:
            session.close()