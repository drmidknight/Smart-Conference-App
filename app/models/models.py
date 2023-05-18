from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import DDL, event, Date, Column,Integer,Boolean,text,String, ForeignKey, TIMESTAMP, BIGINT, MetaData
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
import sqlalchemy as db
from utils.database import *


# #MYSQL_URL = "mysql+pymysql://root:@localhost:3306/fastapi_student_results?charset=utf8"
# MYSQL_URL = "mysql+pymysql://root:Openforme@localhost:3306/smart_conference_app?charset=utf8"
# POOL_SIZE = 20
# POOL_RECYCLE = 3600
# POOL_TIMEOUT = 15
# MAX_OVERFLOW = 2
# CONNECT_TIMEOUT = 60

# connect_argument = {"connect_timeout":CONNECT_TIMEOUT}

# migrate = db.create_engine(MYSQL_URL, pool_size=POOL_SIZE, pool_recycle=POOL_RECYCLE,
#                          pool_timeout=POOL_TIMEOUT, max_overflow=MAX_OVERFLOW, connect_args=connect_argument)

                         
# meta = MetaData()

# Base = declarative_base()

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
