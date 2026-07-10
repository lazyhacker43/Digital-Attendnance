# database.py
# This file sets up our database connection and defines our tables (models).
# We use SQLite instead of MySQL/Postgres for the 7-day sprint — it's a single
# file on your laptop, needs zero setup, and SQL you write against it is
# nearly identical to MySQL. You can migrate to MySQL later if needed.

from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, ForeignKey, Text
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime

# This creates a file called "attendance.db" in your project folder.
DATABASE_URL = "sqlite:///./attendance.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# ---- TABLES (trimmed schema per the 7-day MVP plan) ----

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    role = Column(String(20), nullable=False)  # 'Admin', 'Teacher', 'Student'
    full_name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class BiometricEmbedding(Base):
    __tablename__ = "biometric_embeddings"

    embedding_id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    vector_data = Column(Text, nullable=False)  # store the 128 numbers as a JSON string
    verification_state = Column(String(20), default="Pending")  # Pending / Approved / Rejected
    created_at = Column(DateTime, default=datetime.utcnow)


class ClassSession(Base):
    __tablename__ = "class_sessions"

    session_id = Column(Integer, primary_key=True, index=True)
    teacher_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    session_duration_minutes = Column(Integer, nullable=False)
    snapshot_count = Column(Integer, nullable=False)
    interval_minutes = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class RawTimestamp(Base):
    __tablename__ = "raw_timestamps"

    timestamp_id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("class_sessions.session_id"), nullable=False)
    student_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    scan_number = Column(Integer, nullable=False)
    matched_at = Column(DateTime, default=datetime.utcnow)


class SessionAttendanceStatus(Base):
    __tablename__ = "session_attendance_status"

    status_id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("class_sessions.session_id"), nullable=False)
    student_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    timestamp_count = Column(Integer, nullable=False)
    status = Column(String(20), nullable=False)  # Present / Absent / Pending_Review


# This line actually creates the tables in attendance.db the first time you run the app.
def init_db():
    Base.metadata.create_all(bind=engine)


# FastAPI will call this for every request that needs the database.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
