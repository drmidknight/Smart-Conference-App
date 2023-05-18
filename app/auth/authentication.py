from passlib.context import CryptContext
import jwt
from app.models.models import Admin
from fastapi.exceptions import HTTPException
from fastapi import status
from datetime import datetime, timedelta
from app.utils.config import *
from jose import jwt


pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')



def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=ALGORITHM)
    print(encoded_jwt)
    return encoded_jwt




def get_hashed_password(password):
    return pwd_context.hash(password)



async def verify_token(token: str):
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithm=ALGORITHM)
        user = await Admin.id(id = payload.get('id'))

    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            details="Invalid token",
            headers={"WWW-Authentication": "Bearer"}
        )
    
    return user