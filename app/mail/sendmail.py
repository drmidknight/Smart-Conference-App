from typing import List
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from pydantic import BaseModel, EmailStr
from app.models.models import Participant, Event
from starlette.responses import JSONResponse
from uuid import uuid4
import random
import string
from dotenv  import dotenv_values
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
    MAIL_USERNAME = settings.MAIL_USERNAME,
    MAIL_PASSWORD = settings.MAIL_PASSWORD,
    MAIL_FROM =  settings.MAIL_FROM,
    MAIL_PORT = settings.MAIL_PORT,
    MAIL_SERVER = settings.MAIL_SERVER,
    MAIL_STARTTLS = settings.MAIL_STARTTLS,
    MAIL_SSL_TLS = settings.MAIL_SSL_TLS,
    USE_CREDENTIALS = settings.USE_CREDENTIALS,
    VALIDATE_CERTS = settings.VALIDATE_CERTS
)




def generate_reset_password_token(expires_delta: int = None):
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode = {"exp": expires_delta}
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, settings.ALGORITHM)
    return encoded_jwt




# def generate_reset_password_token(Authorize: AuthJWT = Depends()):
#     expires = timedelta(minutes=3)
#     token = Authorize.create_access_token(subject="test",expires_time=expires)
#     return  token



# def generate_reset_password_token(size=150, chars=string.ascii_lowercase + string.digits):
#     return ''.join(random.choice(chars) for _ in range(size))


# async def read_image():
#     return FileResponse("app/endpoints/images/aiti.png")



# async def send_file(background_tasks: BackgroundTasks,
#     file: UploadFile = File(...),
#     email:EmailStr = Form(...)
#     ) -> JSONResponse:


filename = "app/program_outlines/DBC_COURSE OUTLINE.pdf"


def read_flyer_image():
    return FileResponse("app/flyers/{event_data.flyer}")




async def sendEmailToNewParticipant(email: EmailSchema, instance: Participant):

    event_data = session.query(Event).filter(Event.id == instance.event_id).first()

   
    

    # <img src="app/endpoints/images/{event_data.flyer}" alt="Event Flyer" weight="100" height="100" />
            
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
                    <img src="flyers/{event_data.flyer}" alt="Event Flyer" weight="100" height="100" alt="Event Flyer">
                    <h3>Hi {instance.name}</h3>
                    <p>Welcome to <b>SMART CONFERENCE APP</b></p>
                    <p>Thanks for showing interest in attending the upcoming <b>{event_data.event_name}</b> conference.</p>
                    <p>We will send you a confirmation link for you to confirm your attendance.</p>
                </div>
            </body>
            </html>
    """


    message = MessageSchema(
        subject=" SMART CONFERENCE",
        recipients=email,
        body=html,
        subtype=MessageType.html,
        # attachments=[
        #     {
        #         "file": "/app/endpoints/images/aiti.png",
        #         "headers": {
        #             "Content-ID": "<logo_image@fastapi-mail>",
        #             "Content-Disposition": "inline; filename=\"/app/endpoints/images/aiti.png\" ",  # For inline images only
        #         },
        #         "mime_type": "image",
        #         "mime_subtype": "png",
        #     }
        # ],
        
        )

    fm = FastMail(conf)
    await fm.send_message(message)
    return JSONResponse(status_code=200, content={"message": "email has been sent"})
















async def send_Reset_Password_LinkToStaffEmail(email: EmailSchema, instance: Participant):

    html = f"""                    
                    <br>
                    <p>Hi {instance.admin_name} !</p>
                    <br>
                    <p>You have requested to reset your password. Click on the button below to reset your password</p>

                    <br><br>
                    
                    <a style="margin-top:1rem;padding:1rem;border-radius:0.5rem;font-size:1rem;text-decoration:none;
                    background: #0275d8; color:white;" href="http://localhost:4200/reset-password?token={instance.reset_password_token}">
                    Reset password 
                    </a>
                    <br><br>
                    <p>If you're having problem clicking the Change Password button, copy and paste the URL below into your web browser
                    <br>
                    <b>Link expires in 3 hours</b>
                    </p>
                    http://localhost:4200/reset-password?token={instance.reset_password_token}
                    <br><br>
                    <p><b>Ignore this email if you have not requested to reset your password</b></p>
                    
    """


    message = MessageSchema(
        subject="GHANA-INDIA KOFI ANNAN CENTRE OF EXCELLENCE IN ICT (STUDENT RESULTS APP)",
        recipients=email,
        body=html,
        subtype=MessageType.html)

    fm = FastMail(conf)
    await fm.send_message(message)
    return JSONResponse(status_code=200, content={"message": "email has been sent"})


















async def sendEmailToNewAdmin(email: EmailSchema, instance: Participant):

    html = f"""                    
                    <br>
                    <p>Hi {instance.admin_name} !</p>
                    <br>
                    <p>You have requested to reset your password. Click on the button below to reset your password</p>

                    <br><br>
                    
                    <a style="margin-top:1rem;padding:1rem;border-radius:0.5rem;font-size:1rem;text-decoration:none;
                    background: #0275d8; color:white;" href="http://localhost:4200/reset-password?token={instance.reset_password_token}">
                    Reset password 
                    </a>
                    <br><br>
                    <p>If you're having problem clicking the Change Password button, copy and paste the URL below into your web browser
                    <br>
                    <b>Link expires in 3 hours</b>
                    </p>
                    http://localhost:4200/reset-password?token={instance.reset_password_token}
                    <br><br>
                    <p><b>Ignore this email if you have not requested to reset your password</b></p>
                    
    """


    message = MessageSchema(
        subject="GHANA-INDIA KOFI ANNAN CENTRE OF EXCELLENCE IN ICT (STUDENT RESULTS APP)",
        recipients=email,
        body=html,
        subtype=MessageType.html)

    fm = FastMail(conf)
    await fm.send_message(message)
    return JSONResponse(status_code=200, content={"message": "email has been sent"})