from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Boolean,text,ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
import sqlalchemy as db

                    

Base = declarative_base()


class Participant(Base):
    __tablename__ = 'participants'
    id = db.Column(db.Integer, primary_key=True)
    form_values = db.Column(db.Text, nullable=True)
    status = db.Column(Boolean, default=False, index=False)
    event_id = db.Column(db.Integer, ForeignKey("events.id"))
    created_at = db.Column(TIMESTAMP, nullable=False,server_default=text("CURRENT_TIMESTAMP"))
    updated_at = db.Column(TIMESTAMP, nullable=False,server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    events = relationship("Event", back_populates="participants")








class Event(Base):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    event_name = db.Column(db.String(255), nullable=True, unique=True)
    venue = db.Column(db.String(255), nullable=True)
    flyer = db.Column(db.String(255), nullable=True)
    start_date = db.Column(db.String(255), nullable=True)
    registration_time = db.Column(db.String(255), nullable=True)
    how_to_join = db.Column(db.String(255), nullable=True)
    program_outline = db.Column(db.String(255), nullable=True)
    end_date = db.Column(db.String(255), nullable=True)
    number_of_participants = db.Column(db.String(255), nullable=True)
    description = db.Column(db.String(255), nullable=True)
    admin_id = db.Column(db.Integer, ForeignKey("admins.id"))
    status = db.Column(db.String(255), nullable=True)
    created_at = db.Column(TIMESTAMP, nullable=False,server_default=text("CURRENT_TIMESTAMP"))
    updated_at = db.Column(TIMESTAMP, nullable=False,server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    participants = relationship("Participant", back_populates="events")
    #admins = relationship("Admin", back_populates="event")






class Attendance(Base):
    __tablename__ = 'attendances'
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(255), nullable=True)
    admin_id = db.Column(db.Integer, ForeignKey("admins.id"))
    created_at = db.Column(TIMESTAMP, nullable=False,server_default=text("CURRENT_TIMESTAMP"))
    updated_at = db.Column(TIMESTAMP, nullable=False,server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    participantId = db.Column(db.Integer, ForeignKey("participants.id"))
   # participants = relationship("Participant", back_populates="event")








class ParticipantFields(Base):
    __tablename__ = 'participant_fields'
    id = db.Column(db.Integer, primary_key=True)
    fields = db.Column(db.TEXT, nullable=True)
    event_id = db.Column(db.Integer, ForeignKey('events.id'))
    created_at = db.Column(TIMESTAMP, nullable=False,server_default=text("CURRENT_TIMESTAMP"))
    updated_at = db.Column(TIMESTAMP, nullable=False,server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    #event = relationship("Event", back_populates="participant_fields")



    





class Admin(Base):
    __tablename__ = 'admins'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=True)
    contact = db.Column(db.String(255), nullable=True)
    email = db.Column(db.String(255), nullable=True, unique=True)
    password = db.Column(db.String(255), nullable=True)
    usertype = db.Column(db.String(255), nullable=True)
    reset_password_token = db.Column(db.String(255), nullable=True)
    status = db.Column(db.String(255), nullable=True)
    event_id = db.Column(db.Integer, ForeignKey("events.id"))
    created_at = db.Column(TIMESTAMP, nullable=False,server_default=text("CURRENT_TIMESTAMP"))
    updated_at = db.Column(TIMESTAMP, nullable=False,server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    #event = relationship("Event", back_populates="admins")
    #event = relationship("Event")
    #attendance = relationship("Attendance")












# class Users(Base):
#     __tablename__ = 'users'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(255), nullable=True, unique=True)
#     email = db.Column(db.String(255), nullable=True, unique=True)
#     password = db.Column(db.String(255), nullable=True)
#     reset_password_token = db.Column(db.String(255), nullable=True)
#     status = db.Column(db.String(255), nullable=True)
#     event_id = db.Column(db.Integer, ForeignKey('events.id'))
#     created_at = db.Column(TIMESTAMP, nullable=False,server_default=text("CURRENT_TIMESTAMP"))
#     updated_at = db.Column(TIMESTAMP, nullable=False,server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
#     events = relationship("Event", back_populates="users")
