from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Boolean,text,ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
import sqlalchemy as db

                    

Base = declarative_base()

class Participant(Base):
    __tablename__ = 'participants'
    id = db.Column(db.Integer, primary_key=True, index=True)
    name = db.Column(db.String(255), nullable=True)
    phone_number = db.Column(db.String(255), nullable=True, unique=True)
    gender = db.Column(db.String(255), nullable=True)
    email = db.Column(db.String(255), nullable=True, unique=True, index=True)
    organization = db.Column(db.String(255), nullable=True)
    status = db.Column(Boolean, default=False, index=False)
    attend_by = db.Column(db.String(255), nullable=True)
    registration_time = db.Column(db.String(255), nullable=True)
    location = db.Column(db.String(255), nullable=True)
    event_id = db.Column(db.Integer, ForeignKey('events.id'))
    created_at = db.Column(TIMESTAMP, nullable=False,server_default=text("CURRENT_TIMESTAMP"))
    updated_at = db.Column(TIMESTAMP, nullable=False,server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    event = relationship("Event", back_populates="participants")
    #attendance_id = db.Column(db.Integer, ForeignKey('attendances.id'))




class Event(Base):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True, index=True)
    event_name = db.Column(db.String(255), nullable=True, unique=True)
    venue = db.Column(db.String(255), nullable=True)
    flyer = db.Column(db.String(255), nullable=True)
    start_date = db.Column(db.String(255), nullable=True)
    registration_time = db.Column(db.String(255), nullable=True)
    end_date = db.Column(db.String(255), nullable=True)
    number_of_participants = db.Column(db.Integer)
    description = db.Column(db.String(255), nullable=True)
    admin_id = db.Column(db.Integer, ForeignKey("admins.id"))
    status = db.Column(db.String(255), nullable=True)
    created_at = db.Column(TIMESTAMP, nullable=False,server_default=text("CURRENT_TIMESTAMP"))
    updated_at = db.Column(TIMESTAMP, nullable=False,server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    participants = relationship("Participant", back_populates="event")


class Attendance(Base):
    __tablename__ = 'attendances'
    id = db.Column(db.Integer, primary_key=True, index=True)
    status = db.Column(db.String(255), nullable=True)
    admin_id = db.Column(db.Integer, ForeignKey("admins.id"))
    created_at = db.Column(TIMESTAMP, nullable=False,server_default=text("CURRENT_TIMESTAMP"))
    updated_at = db.Column(TIMESTAMP, nullable=False,server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    participantId = db.Column(db.Integer, ForeignKey("participants.id"))
   # participants = relationship("Participant", back_populates="event")


class Admin(Base):
    __tablename__ = 'admins'
    id = db.Column(db.Integer, primary_key=True, index=True)
    admin_name = db.Column(db.String(255), nullable=True, unique=True)
    contact = db.Column(db.String(255), nullable=True, unique=True)
    email = db.Column(db.String(255), nullable=True, unique=True, index=True)
    password = db.Column(db.String(255), nullable=True)
    reset_password_token = db.Column(db.String(255), nullable=True)
    status = db.Column(db.String(255), nullable=True)
    created_at = db.Column(TIMESTAMP, nullable=False,server_default=text("CURRENT_TIMESTAMP"))
    updated_at = db.Column(TIMESTAMP, nullable=False,server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    event = relationship("Event")
    attendance = relationship("Attendance")
