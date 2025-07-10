import datetime
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Boolean, LargeBinary, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from .config import settings

# --- Database Setup ---
DATABASE_URL = f"sqlite:///{settings.database_path}"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# --- Models ---
class Note(Base):
    __tablename__ = "notes"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    encrypted_content = Column(LargeBinary, nullable=False)
    tags = Column(String(200), default="")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    is_pinned = Column(Boolean, default=False)
    is_deleted = Column(Boolean, default=False)
    is_archived = Column(Boolean, default=False)
    
    revisions = relationship("NoteRevision", back_populates="note", cascade="all, delete-orphan")

class NoteRevision(Base):
    __tablename__ = "note_revisions"
    id = Column(Integer, primary_key=True, index=True)
    note_id = Column(Integer, ForeignKey("notes.id"), nullable=False)
    encrypted_content = Column(LargeBinary, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    note = relationship("Note", back_populates="revisions")

class Template(Base):
    __tablename__ = "templates"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    content = Column(Text, nullable=False)

def init_db():
    Base.metadata.create_all(bind=engine) 