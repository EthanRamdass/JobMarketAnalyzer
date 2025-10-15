# backend/models.py
import os
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, func, Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///jobs.db")
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class Job(Base):
    __tablename__ = "jobs"
    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(String, unique=True, index=True)  # dedup key
    title = Column(String, index=True)
    company = Column(String, index=True)
    location = Column(String, index=True)
    date_posted = Column(DateTime)
    description = Column(Text)
    url = Column(String)
    tags = Column(String)  # CSV list of tags/skills

    __table_args__ = (
        Index("ix_title_company", "title", "company"),
    )

def init_db():
    Base.metadata.create_all(bind=engine)

def get_db_session():
    return SessionLocal()



