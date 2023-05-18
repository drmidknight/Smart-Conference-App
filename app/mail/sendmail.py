from typing import List
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from pydantic import BaseModel, EmailStr
from app.models.models import Admin
from starlette.responses import JSONResponse
from uuid import uuid4
import random
import string
from dotenv  import dotenv_values
from fastapi import Depends
from fastapi_jwt_auth import AuthJWT
from datetime import datetime, time, timedelta
from app.utils.config import *
from jose import jwt


config_credentials = dotenv_values(".env")


class EmailSchema(BaseModel):
    email: List[EmailStr]



conf = ConnectionConfig(
    # MAIL_USERNAME = config_credentials["EMAIL"],
    # MAIL_PASSWORD = config_credentials["PASSWORD"],
    # MAIL_FROM =  config_credentials["EMAIL"],
    MAIL_USERNAME = "bismarkotu1006@gmail.com",
    MAIL_PASSWORD ="olimwedzhheuxfce",
    MAIL_FROM =  "bismarkotu1006@gmail.com",
    MAIL_PORT = 587,
    MAIL_SERVER = "smtp.gmail.com",
    MAIL_STARTTLS = True,
    MAIL_SSL_TLS = False,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = True
)




def generate_reset_password_token(expires_delta: int = None):
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode = {"exp": expires_delta}
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, ALGORITHM)
    return encoded_jwt




# def generate_reset_password_token(Authorize: AuthJWT = Depends()):
#     expires = timedelta(minutes=3)
#     token = Authorize.create_access_token(subject="test",expires_time=expires)
#     return  token



# def generate_reset_password_token(size=150, chars=string.ascii_lowercase + string.digits):
#     return ''.join(random.choice(chars) for _ in range(size))




async def sendEmailToNewAdmin(email: EmailSchema, instance: Admin):

    html = f"""                    
                    <br>
                    <p>Hi {instance.admin_name} !</p>
                    <br>
                    <p>You have been added to <b>SMART CONFERENCE APP</b> as an Admin</p>
                    <br><br>
                    Change your password to access the application.
                    <br><br>
                    
                    <a style="margin-top:1rem;padding:1rem;border-radius:0.5rem;font-size:1rem;text-decoration:none;
                    background: #0275d8; color:white;" href="http://localhost:4200/reset-password?token={instance.reset_password_token}">
                    Change password 
                    </a>
                    <br><br>
                    <p>If you're having problem clicking the Change Password button, copy and paste the URL below into your web browser</p>
                    http://localhost:4200/reset-password?token={instance.reset_password_token}
                    
    """


    message = MessageSchema(
        subject="SMART CONFERENCE APP",
        recipients=email,
        body=html,
        subtype=MessageType.html)

    fm = FastMail(conf)
    await fm.send_message(message)
    return JSONResponse(status_code=200, content={"message": "email has been sent"})
















async def send_Reset_Password_LinkToStaffEmail(email: EmailSchema, instance: Admin):

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