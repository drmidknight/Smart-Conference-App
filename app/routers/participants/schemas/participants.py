from fastapi import Form
from pydantic import BaseModel, EmailStr, Field
from fastapi import Form
from typing import Optional




class ParticipantRequest(BaseModel):
    name:Optional[str] = None
    phone_number:Optional[str] = None
    gender:Optional[str] = None
    email:Optional[str] = None
    organization:Optional[str] = None
    how_to_join:Optional[str] = None
    registration_time:Optional[str] = None
    location:Optional[str] = None
    event_id: Optional[int] = None




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
    field_validation:Optional[int]
    field_max_length:Optional[int]
    field_min_length:Optional[int]
    event_id:Optional[int]




class UpdateParticipantField(BaseModel):
    id:Optional[int]
    field_name:Optional[str]
    field_type:Optional[str]
    field_validation:Optional[int]
    field_max_length:Optional[int]
    field_min_length:Optional[int]
    event_id:Optional[int]
