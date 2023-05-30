from pydantic import BaseModel, EmailStr, Field
from fastapi import Form
from typing import Optional




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
