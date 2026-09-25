from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Float, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "sqlite:///./ayuripr.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class Source(Base):
    __tablename__ = "sources"
    id = Column(Integer, primary_key=True)
    title = Column(String(500), nullable=False)
    jurisdiction = Column(String(50), nullable=False)
    source_type = Column(String(100), nullable=False)
    authority = Column(String(250), nullable=False)
    url = Column(String(1000), nullable=False)
    section = Column(String(250))
    version = Column(String(100))
    effective_date = Column(String(50))
    text = Column(Text, nullable=False)
    verified = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class Assessment(Base):
    __tablename__ = "assessments"
    id = Column(Integer, primary_key=True)
    question = Column(Text, nullable=False)
    jurisdiction = Column(String(50), nullable=False)
    product_category = Column(String(100))
    confidence = Column(Float)
    result_json = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(bind=engine)
