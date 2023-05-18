from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import DDL, event, Date,Column,Integer,Boolean,text,String, ForeignKey, TIMESTAMP, BIGINT, MetaData
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
import sqlalchemy as db
from utils.database import *




class Participant(Base):
    __tablename__ = 'participants'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=True)
    phone_number = Column(String(255), nullable=True, unique=True)
    gender = Column(String(255), nullable=True)
    email = Column(String(255), nullable=True, unique=True, index=True)
    organization = Column(String(255), nullable=True)
    status = Column(Boolean, default=False, index=False)
    attend_by = Column(String(255), nullable=True)
    registration_time = Column(String(255), nullable=True)
    location = Column(String(255), nullable=True)
    event_id = Column(Integer, ForeignKey('events.id'))
    created_at = db.Column(TIMESTAMP, nullable=False,server_default=text("CURRENT_TIMESTAMP"))
    updated_at = db.Column(TIMESTAMP, nullable=False,server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    event = relationship("Event", back_populates="participants")
    #attendance_id = Column(Integer, ForeignKey('attendances.id'))




class Event(Base):
    __tablename__ = 'events'
    id = Column(Integer, primary_key=True, index=True)
    event_name = Column(String(255), nullable=True, unique=True)
    venue = Column(String(255), nullable=True)
    image = Column(String(255), nullable=True)
    start_date = Column(String(255), nullable=True)
    end_date = Column(String(255), nullable=True)
    number_of_participants = Column(Integer)
    description = Column(String(255), nullable=True)
    admin_id = Column(Integer, ForeignKey("admins.id"))
    created_at = db.Column(TIMESTAMP, nullable=False,server_default=text("CURRENT_TIMESTAMP"))
    updated_at = db.Column(TIMESTAMP, nullable=False,server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    participants = relationship("Participant", back_populates="event")


class Attendance(Base):
    __tablename__ = 'attendances'
    id = Column(Integer, primary_key=True, index=True)
    status = Column(String(255), nullable=True)
    admin_id = Column(Integer, ForeignKey("admins.id"))
    created_at = db.Column(TIMESTAMP, nullable=False,server_default=text("CURRENT_TIMESTAMP"))
    updated_at = db.Column(TIMESTAMP, nullable=False,server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    participantId = Column(Integer, ForeignKey("participants.id"))
   # participants = relationship("Participant", back_populates="event")


class Admin(Base):
    __tablename__ = 'admins'
    id = Column(Integer, primary_key=True, index=True)
    admin_name = Column(String(255), nullable=True, unique=True)
    contact = Column(String(255), nullable=True, unique=True)
    email = Column(String(255), nullable=True, unique=True, index=True)
    password = Column(String(255), nullable=True)
    reset_password_token = Column(String(255), nullable=True)
    status = Column(String(255), nullable=True)
    created_at = db.Column(TIMESTAMP, nullable=False,server_default=text("CURRENT_TIMESTAMP"))
    updated_at = db.Column(TIMESTAMP, nullable=False,server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    event = relationship("Event")
    attendance = relationship("Attendance")
