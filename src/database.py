import os

from dotenv import load_dotenv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(dotenv_path=BASE_DIR / ".env")

from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncAttrs

from sqlalchemy import Column, ForeignKey, Integer, String, Text, Boolean, DateTime, func, select, text


Base = declarative_base(cls=AsyncAttrs)

DB_URL = os.getenv("ALLTALE_DB_URL")
engine = create_async_engine(DB_URL, echo=True, future=True)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(String(95), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    is_active = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime, nullable=False, server_default=func.now())

    passages = relationship('Passage', back_populates='creator')
    sessions = relationship('Session', back_populates='user')

class Session(Base):
    __tablename__ = 'session'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=True, index=True)
    session_token = Column(String(64), unique=True, nullable=False)
    expire_at = Column(DateTime, nullable=False)

    ip_address = Column(String(45), nullable=True)
    user_agent = Column(String(255), nullable=True)
    csrf_token = Column(String(64), nullable=True)

    user = relationship('User', back_populates='sessions')


OT_BOOKS = {
    "Genesis","Exodus","Leviticus","Numbers","Deuteronomy","Joshua","Judges","Ruth",
    "1 Samuel","2 Samuel","1 Kings","2 Kings","1 Chronicles","2 Chronicles",
    "Ezra","Nehemiah","Esther","Job","Psalms","Proverbs","Ecclesiastes","Song of Solomon",
    "Isaiah","Jeremiah","Lamentations","Ezekiel","Daniel","Hosea","Joel","Amos","Obadiah",
    "Jonah","Micah","Nahum","Habakkuk","Zephaniah","Haggai","Zechariah","Malachi"
}

translations_path = [
    "res/scriptures/en/kjv.json",
    "res/scriptures/en/web.json",
    "res/scriptures/tl/tagab.json"
]
class Scriptures(Base):
    __tablename__ = "scriptures"

    translation = Column(String(10), primary_key=True)
    book_index = Column(Integer, primary_key=True)
    chapter = Column(Integer, primary_key=True)
    verse = Column(Integer, primary_key=True)
    book_name = Column(String(50), nullable=False, index=True)
    text = Column(Text, nullable=False)
    testament = Column(String(2), nullable=False, index=True)


class Passage(Base):
    __tablename__ = 'passage'

    id = Column(Integer, primary_key=True)
    epitome = Column(String, nullable=False)
    text = Column(Text, nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    is_active = Column(Boolean, nullable=False, default=False)

    creator_id = Column(Integer, ForeignKey('user.id'), nullable=False, index=True)
    creator = relationship('User', back_populates='passages')

    seals = relationship('PassageSeal', back_populates='passage')
    prayers = relationship('Prayer', back_populates='passage')
    bible_links = relationship('PassageBibleLink', back_populates='passage')

class Seal(Base):
    __tablename__ = 'seal'

    id = Column(Integer, primary_key=True)
    name = Column(String(120), unique=True, nullable=False)

    passages = relationship('PassageSeal', back_populates='seal')

class PassageSeal(Base):
    __tablename__ = 'passage_seal'

    passage_id = Column(Integer, ForeignKey('passage.id'), primary_key=True)
    seal_id = Column(Integer, ForeignKey('seal.id'), primary_key=True)

    seal = relationship('Seal', back_populates='passages')
    passage = relationship('Passage', back_populates='seals')
    
class Prayer(Base):
    __tablename__ = "prayer"

    id = Column(Integer, primary_key=True)
    passage_id = Column(Integer, ForeignKey('passage.id'), nullable=False, index=True)
    text = Column(Text, nullable=False)
    index = Column(Integer, nullable=False)

    passage = relationship('Passage', back_populates='prayers')

class PassageBibleLink(Base):
    __tablename__ = "passage_bible_link"

    id = Column(Integer, primary_key=True)
    passage_id = Column(Integer, ForeignKey('passage.id'), nullable=False, index=True)
    book = Column(String(50), nullable=False, index=True)
    chapter_start = Column(Integer, nullable=False, index=True)
    verse_start = Column(Integer, nullable=True)
    chapter_end = Column(Integer, nullable=True)
    verse_end = Column(Integer, nullable=True)
    is_foundation = Column(Boolean, nullable=False)
    index = Column(Integer, nullable=False)

    passage = relationship('Passage', back_populates='bible_links')


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
