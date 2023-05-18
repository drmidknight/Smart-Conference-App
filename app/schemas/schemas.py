from pydantic import BaseModel, EmailStr, Field
from typing import Optional






class AdminRequest(BaseModel):
    admin_name:str
    email:str
    contact:str



class UpdateAdmin(BaseModel):
    id:Optional[int]
    admin_name:Optional[str]
    contact:Optional[str]
    email:Optional[str]




class TokenPayload(BaseModel):
    email: str = None
    contact: str = None
    exp: int = None



class ShowAdmin(BaseModel):
    id: int
    email: str



class LoginModel(BaseModel):
    email:str
    password:str



class Settings(BaseModel):
    authjwt_secret_key:str='f7ba61299699cb4ca16a09a5ee5fe6aa3db551acf4a5959c1063f7320c13a77e'