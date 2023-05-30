from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Boolean,text,ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
import sqlalchemy as db

                    

Base = declarative_base()





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
    number_of_participants = db.Column(db.Integer)
    description = db.Column(db.String(255), nullable=True)
    admin_id = db.Column(db.Integer, ForeignKey("admins.id"))
    status = db.Column(db.String(255), nullable=True)
    created_at = db.Column(TIMESTAMP, nullable=False,server_default=text("CURRENT_TIMESTAMP"))
    updated_at = db.Column(TIMESTAMP, nullable=False,server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    participants = relationship("Participant", back_populates="event")
