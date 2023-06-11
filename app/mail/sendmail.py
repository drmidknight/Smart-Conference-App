from typing import List
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from pydantic import BaseModel, EmailStr
from app.models.models import Participant, Event
from starlette.responses import JSONResponse
from uuid import uuid4
import random
import string
from dotenv import dotenv_values
from fastapi import Depends, File, UploadFile, Form, BackgroundTasks
from fastapi_jwt_auth import AuthJWT
from datetime import datetime, time, timedelta
from app.utils.config import *
from jose import jwt
from app.utils.database import Database
from app.utils.config import settings
from fastapi.responses import FileResponse
import shutil


config_credentials = dotenv_values(".env")

database = Database()
engine = database.get_db_connection()
session = database.get_db_session(engine)


class EmailSchema(BaseModel):
    email: List[EmailStr]


PROGRAMOUTLINEDIR = "app/program_outlines/"

conf = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_STARTTLS=settings.MAIL_STARTTLS,
    MAIL_SSL_TLS=settings.MAIL_SSL_TLS,
    USE_CREDENTIALS=settings.USE_CREDENTIALS,
    VALIDATE_CERTS=settings.VALIDATE_CERTS
)


def generate_reset_password_token(expires_delta: int = None):
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode = {"exp": expires_delta}
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, settings.ALGORITHM)
    return encoded_jwt


async def sendEmailToNewParticipant(email: EmailSchema, instance: Participant):
    event_data = session.query(Event).filter(Event.id == instance.event_id).first()
    flyer_name = event_data.flyer
    flyer = FileResponse(f"app/flyers/{flyer_name}")

    html = f"""
            <!doctype html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>{event_data.event_name} CONFERENCE</title>
                <style>
                    body {{
                        font-family: Arial, sans-serif;
                        background-color: #f1f1f1;
                        margin: 0;
                        padding: 0;
                    }}

                    .container {{
                        display: flex;
                        flex-direction: column;
                        align-items: center;
                        justify-content: center;
                        text-align: center;
                        padding: 40px;
                        background-color: #ffffff;
                        box-shadow: 0px 2px 10px rgba(0, 0, 0, 0.1);
                        border-radius: 5px;
                        max-width: 400px;
                        margin: 0 auto;
                        margin-top: 40px;
                    }}

                    .container img {{
                        max-width: 100%;
                        margin-bottom: 20px;
                        border-radius: 5px;
                    }}

                    h3, p {{
                        margin: 0;
                        margin-bottom: 10px;
                    }}
                </style>
            </head>
            <body>
                <div class="container">
                    <img src="{flyer.url}" alt="Event Flyer">
                    <h3>Hi {instance.name}</h3>
                    <p>Welcome to <b>SMART CONFERENCE APP</b></p>
                    <p>Thanks for showing interest in attending the upcoming <b>{event_data.event_name}</b> conference.</p>
                    <p>We will send you a confirmation link for you to confirm your attendance.</p>
                </div>
            </body>
            </html>
    """

    message = MessageSchema(
        subject=" {event_data.event_name} CONFERENCE",
        recipients=email,
        body=html,
        subtype=MessageType.html,
    )

    fm = FastMail(conf)
    await fm.send_message(message)
    return JSONResponse(status_code=200, content={"message": "email has been sent"})
