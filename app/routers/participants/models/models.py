from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Boolean,text,ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
import sqlalchemy as db

                    

Base = declarative_base()



class Participant(Base):
    __tablename__ = 'participants'
    id = db.Column(db.Integer, primary_key=True)
    form_values = db.Column(db.JSON, nullable=True)
    status = db.Column(Boolean, default=False, index=False)
    event_id = db.Column(db.Integer, ForeignKey('events.id'))
    created_at = db.Column(TIMESTAMP, nullable=False,server_default=text("CURRENT_TIMESTAMP"))
    updated_at = db.Column(TIMESTAMP, nullable=False,server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))













class ParticipantFields(Base):
    __tablename__ = 'participant_fields'
    id = db.Column(db.Integer, primary_key=True)
    fields = db.Column(db.JSON, nullable=True)
    event_id = db.Column(db.Integer, ForeignKey('events.id'))
    created_at = db.Column(TIMESTAMP, nullable=False,server_default=text("CURRENT_TIMESTAMP"))
    updated_at = db.Column(TIMESTAMP, nullable=False,server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))























# class ParticipantFields(Base):
#     __tablename__ = 'participant_fields'
#     id = db.Column(db.Integer, primary_key=True)
#     field_name = db.Column(db.String(255), nullable=True)
#     field_type = db.Column(db.String(255), nullable=True, unique=True)
#     field_validation = db.Column(db.String(255), nullable=True)
#     field_max_length = db.Column(db.String(255), nullable=True, unique=True)
#     field_min_length = db.Column(db.String(255), nullable=True)
#     status = db.Column(Boolean, default=False, index=False)
#     event_id = db.Column(db.Integer, ForeignKey('events.id'))
#     created_at = db.Column(TIMESTAMP, nullable=False,server_default=text("CURRENT_TIMESTAMP"))
#     updated_at = db.Column(TIMESTAMP, nullable=False,server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
#     #event = relationship("Event", back_populates="participant_fields")