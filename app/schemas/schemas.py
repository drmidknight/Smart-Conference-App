from pydantic import BaseModel, EmailStr, Field
from fastapi import Form
from typing import Optional



class AdminRequest(BaseModel):
    admin_name:str
    email:str
    contact:str

    class Config():
        orm_mode = True


class UpdateAdmin(BaseModel):
    id:Optional[int]
    admin_name:Optional[str]
    contact:Optional[str]
    email:Optional[str]

    class Config():
        orm_mode = True





class EventRequest(BaseModel):
    event_name:Optional[str]
    venue:Optional[str]
    start_date:Optional[str]
    end_date:Optional[str]
    registration_time:Optional[str]
    how_to_join:Optional[str]
    number_of_participants:Optional[str]
    description:Optional[str]

    class Config():
        orm_mode = True



class UpdateEventRequest(BaseModel):
    id:Optional[int]
    event_name:Optional[str]
    venue:Optional[str]
    start_date:Optional[str]
    end_date:Optional[str]
    registration_time:Optional[str]
    flyer:Optional[str]
    number_of_participants:Optional[str]
    how_to_join:Optional[str]
    program_outline:Optional[str]
    description:Optional[str]





class ParticipantRequest(BaseModel):
    name:Optional[str]
    phone_number:Optional[str]
    gender:Optional[str]
    email:Optional[str]
    organization:Optional[str]
    attend_by:Optional[str]
    registration_time:Optional[str]
    location:Optional[str]
    event_id: Optional[int]




class UpdateParticipant(BaseModel):
    id:Optional[int]
    name:Optional[str]
    phone_number:Optional[str]
    gender:Optional[str]
    email:Optional[str]
    organization:Optional[str]
    attend_by:Optional[str]
    registration_time:Optional[str]
    location:Optional[str]
    event_id: Optional[int]




class TokenPayload(BaseModel):
    email: str = None
    contact: str = None
    exp: int = None



class TokenData(BaseModel):
    username: str | None = None
    scopes: list[str] = []


class Token(BaseModel):
    access_token: str
    token_type: str

    
class ShowAdmin(BaseModel):
    id: int
    email: str



class LoginModel(BaseModel):
    email:Optional[str]
    password:Optional[str]



class Settings(BaseModel):
    authjwt_secret_key:str='f7ba61299699cb4ca16a09a5ee5fe6aa3db551acf4a5959c1063f7320c13a77e'