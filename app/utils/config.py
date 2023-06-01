import secrets
from pydantic import BaseSettings


class Settings(BaseSettings):
    MYSQL_SERVER: str = 'localhost'
    MYSQL_USER: str = 'root'
    MYSQL_PASSWORD: str = ''
    MYSQL_DB: str = 'conference_app'

    SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:@localhost:3307/smart_conference_app?charset=utf8"

    EMAIL_CODE_DURATION_IN_MINUTES: int = 15
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_DURATION_IN_MINUTES: int = 600
    PASSWORD_RESET_TOKEN_DURATION_IN_MINUTES: int = 15
    ACCOUNT_VERIFICATION_TOKEN_DURATION_IN_MINUTES: int = 15

    POOL_SIZE = 20
    POOL_RECYCLE = 3600
    POOL_TIMEOUT = 15
    MAX_OVERFLOW = 2
    CONNECT_TIMEOUT = 60
    connect_args = {"connect_timeout":CONNECT_TIMEOUT}



    MAIL_USERNAME: str = 'obwebsitedesign@gmail.com'
    MAIL_PASSWORD: str = 'mqzcxllgcoprfxia'
    MAIL_FROM: str = 'obwebsitedesign@gmail.com'
    MAIL_PORT: int = 587
    MAIL_SERVER: str = 'smtp.gmail.com'
    MAIL_STARTTLS = True
    MAIL_SSL_TLS = False
    USE_CREDENTIALS = True
    VALIDATE_CERTS = True

    TWILIO_PHONE_NUMBER: str = '+16196584362'
    TWILIO_AUTH_TOKEN: str = '7b6c506ee07337cc3d02536d5119c4b2'
    TWILIO_ACCOUNT_SID: str = 'AC959cbde01aced5669b0121ffea2df117'


    #JWT_SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    JWT_SECRET_KEY : str = secrets.token_urlsafe(32)
    ALGORITHM = "HS256"
    #ACCESS_TOKEN_EXPIRE_MINUTES = 2

    class Config:
        case_sensitive = True

        # If you want to read environment variables from a .env
        # file instead un-comment the below line and create the
        # .env file at the root of the project.

        env_file = ".env"

settings = Settings()
