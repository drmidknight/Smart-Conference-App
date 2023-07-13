from passlib.context import CryptContext
import jwt
from models.models import Admin
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from fastapi import status, Security
from datetime import datetime, timedelta
from pydantic import ValidationError
from utils.config import *
from jose import JWTError, jwt
from fastapi.security import (OAuth2PasswordBearer, SecurityScopes)
from routers.admin.schemas.admin import *
from routers.admin.endpoint.admin import *
from typing import Optional
from utils.database import *
from utils.config import settings


pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="admin/login",  scheme_name="JWT",
scopes={"me": "Read information about the current user.", "items": "Read items."})


database = Database()
engine = database.get_db_connection()
session = database.get_db_session(engine)



def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=60)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt




def get_hashed_password(password):
    return pwd_context.hash(password)





def generate_reset_password_token(expires_delta: int = None):
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode = {"exp": expires_delta}
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, settings.ALGORITHM)
    return encoded_jwt





def verify_token(token: str):
    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET_KEY, algorithms=settings.ALGORITHM
        )
        token_data = TokenPayload(**payload)
        print(payload)
        
        if datetime.fromtimestamp(token_data.exp) < datetime.now():
            raise HTTPException(
                status_code = status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except JWTError:
            raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
   
    admin = getAdminByEmail(token_data.email)
    if admin is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not find Admin",
        )
    

    return admin







def get_user(username: str):
    return session.query(Admin).filter(Admin.email== username).first()


def admin_db():
    data = session.query(Admin).filter(Admin.status == "Active").all()
    return data



async def get_current_user(
    security_scopes: SecurityScopes, token: str = Depends(oauth2_scheme)
):
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = "Bearer"
        credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": authenticate_value},
    )
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("email")
        if email is None:
            raise credentials_exception
        token_scopes = payload.get("scopes", [])
        token_data = TokenData(scopes=token_scopes, username=email)
    except (JWTError, ValidationError):
        raise credentials_exception
    user = get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    for scope in security_scopes.scopes:
        if scope not in token_data.scopes:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not enough permissions",
                headers={"WWW-Authenticate": authenticate_value},
            )
    return user


async def get_current_active_user(
    current_user: Admin = Security(get_current_user, scopes=["me"])
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user