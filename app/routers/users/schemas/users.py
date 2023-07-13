from pydantic import BaseModel, EmailStr, Field
from fastapi import Form
from typing import Optional



class UserRequest(BaseModel):
    name:str
    email:str

    class Config():
        orm_mode = True


class UpdateUser(BaseModel):
    id:Optional[int]
    name:Optional[str]
    email:Optional[str]

    class Config():
        orm_mode = True




class TokenPayload(BaseModel):
    email: str = None
    contact: str = None
    exp: int = None



class TokenData(BaseModel):
    username: str = None
    scopes: list[str] = []


class Token(BaseModel):
    access_token: str
    token_type: str

    
class ShowUser(BaseModel):
    id: int
    email: str



class LoginModel(BaseModel):
    email:Optional[str]
    password:Optional[str]



class Settings(BaseModel):
    authjwt_secret_key:str='f7ba61299699cb4ca16a09a5ee5fe6aa3db551acf4a5959c1063f7320c13a77e'