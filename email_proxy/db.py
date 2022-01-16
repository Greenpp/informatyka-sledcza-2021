from sqlalchemy import Column, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.types import Boolean, Integer, String, Text

from .settings import DB_URL

Base = declarative_base()

class Email(Base):
    __tablename__ = 'emails'

    id = Column(Integer(), primary_key=True)
    sender = Column(String(255), nullable=False)
    receiver = Column(String(255), nullable=False)
    subject = Column(String(1023), nullable=False)
    msg = Column(Text())
    is_dangerous = Column(Boolean(), nullable=False)
    

class Attachment(Base):
    __tablename__ = 'attachments'

    id = Column(Integer(), primary_key=True)
    hash_ = Column('hash', String(255), nullable=False)
    is_dangerous = Column(Boolean(), nullable=False)


engine = create_engine(DB_URL)
Base.metadata.create_all(engine)
session_factory = sessionmaker(engine)
