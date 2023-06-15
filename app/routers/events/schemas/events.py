from pydantic import BaseModel, EmailStr, Field
from fastapi import File, UploadFile, Form
from typing import Optional







class EventRequest(BaseModel):
    event_name:Optional[str]
    venue:Optional[str]
    start_date:Optional[str]
    end_date:Optional[str]
    registration_time:Optional[str]
    how_to_join:Optional[str]
    number_of_participants:Optional[str]
    description:Optional[str]
    # flyer: UploadFile = File(None)
    # program_outline: UploadFile = File(None)

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
