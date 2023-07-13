from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import text, TIMESTAMP,ForeignKey
from sqlalchemy.orm import relationship
import sqlalchemy as db

                    

Base = declarative_base()



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