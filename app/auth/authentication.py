from passlib.context import CryptContext
import jwt
from app.models.models import Admin
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from fastapi import status, Security
from datetime import datetime, timedelta
from app.utils.config import *
from jose import JWTError, jwt
from fastapi.security import (OAuth2PasswordBearer, OAuth2PasswordRequestForm)
from app.schemas.schemas import *
from app.endpoints.admin import *
from app.utils.database import *


pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="admin/login",  scheme_name="JWT" )



def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=ALGORITHM)
    print(encoded_jwt)
    return encoded_jwt




def get_hashed_password(password):
    return pwd_context.hash(password)





def verify_token(token: str):
    try:
        payload = jwt.decode(
            token, JWT_SECRET_KEY, algorithms=ALGORITHM
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





async def get_current_user(data: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    
    return verify_token(data, db)

def get_current_active_user(
    current_admin = Security(get_current_user)):

     return current_admin






# async def verify_token(token: str):
#     try:
#         payload = jwt.decode(token, JWT_SECRET_KEY, algorithm=ALGORITHM)
#         user = await Admin.id(id = payload.get('id'))

#     except:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             details="Invalid token",
#             headers={"WWW-Authentication": "Bearer"}
#         )
    
#     return user