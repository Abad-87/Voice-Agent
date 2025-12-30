from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, Float, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    full_name = Column(String)
    phone = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    appointments = relationship("Appointment", back_populates="user")
    medications = relationship("Medication", back_populates="user")
    health_logs = relationship("HealthLog", back_populates="user")

class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    doctor_name = Column(String)
    specialty = Column(String)
    appointment_datetime = Column(DateTime)
    status = Column(String, default="scheduled")  # scheduled, completed, cancelled
    notes = Column(Text)
    reminder_sent = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="appointments")

class Medication(Base):
    __tablename__ = "medications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String)
    dosage = Column(String)
    frequency = Column(String)
    start_date = Column(DateTime)
    end_date = Column(DateTime, nullable=True)
    reminder_time = Column(String)  # e.g., "08:00,14:00,20:00"
    refill_alert = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="medications")

class HealthLog(Base):
    __tablename__ = "health_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    log_type = Column(String)  # daily_check, symptom, mood, etc.
    data = Column(JSON)  # Store structured health data
    urgency_level = Column(String, default="low")  # low, medium, emergency
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="health_logs")

class ClinicalNote(Base):
    __tablename__ = "clinical_notes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    doctor_id = Column(Integer, nullable=True)  # For doctor-side notes
    note_type = Column(String)  # soap, dictation, etc.
    subjective = Column(Text)
    objective = Column(Text)
    assessment = Column(Text)
    plan = Column(Text)
    raw_transcript = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="clinical_notes")
