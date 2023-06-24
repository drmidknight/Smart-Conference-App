from fastapi import Form
from pydantic import BaseModel, EmailStr, Field
from fastapi import Form
from typing import Optional




class ParticipantRequest(BaseModel):
    name:Optional[str]
    phone_number:Optional[str]
    gender:Optional[str]
    email:Optional[str]
    organization:Optional[str]
    how_to_join:Optional[str]
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
    how_to_join:Optional[str]
    registration_time:Optional[str]
    location:Optional[str]
    event_id: Optional[int]
























class ParticipantFieldRequest(BaseModel):
    field_name:Optional[str]
    field_type:Optional[str]
    field_validation:Optional[str]
    field_max_length:Optional[str]
    field_min_length:Optional[str]
    event_id:Optional[int]

    class Config:
        orm_mode = True




class UpdateParticipantField(BaseModel):
    id:Optional[int]
    field_name:Optional[str]
    field_type:Optional[str]
    field_validation:Optional[str]
    field_max_length:Optional[str]
    field_min_length:Optional[str]
    event_id:Optional[int]
