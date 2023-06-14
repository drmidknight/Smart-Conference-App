from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import text, TIMESTAMP
from sqlalchemy.orm import relationship
import sqlalchemy as db

                    

Base = declarative_base()



class Admin(Base):
    __tablename__ = 'admins'
    id = db.Column(db.Integer, primary_key=True)
    admin_name = db.Column(db.String(255), nullable=True, unique=True)
    contact = db.Column(db.String(255), nullable=True, unique=True)
    email = db.Column(db.String(255), nullable=True, unique=True)
    password = db.Column(db.String(255), nullable=True)
    reset_password_token = db.Column(db.String(255), nullable=True)
    status = db.Column(db.String(255), nullable=True)
    created_at = db.Column(TIMESTAMP, nullable=False,server_default=text("CURRENT_TIMESTAMP"))
    updated_at = db.Column(TIMESTAMP, nullable=False,server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    # event = relationship("Event")
    # attendance = relationship("Attendance")
