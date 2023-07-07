from fastapi import Form
from pydantic import BaseModel, EmailStr, Field
from fastapi import Form
from typing import Any, Callable, List, Optional, Sequence
from pydantic.fields import ModelField





class ParticipantRequest(BaseModel):
    form_values:Optional[str]
    event_id: Optional[int]


    class Config:
        orm_mode = True


# class ParticipantRequest(BaseModel):
#     name:Optional[str]
#     full_name:Optional[str]
#     first_name:Optional[str]
#     last_name:Optional[str]
#     other_name:Optional[str]
#     phone_number:Optional[str]
#     contact:Optional[str]
#     gender:Optional[str]
#     email:Optional[str]
#     address:Optional[str]
#     how_to_join:Optional[str]
#     registration_time:Optional[str]
#     organization:Optional[str]
#     time:Optional[str]
#     location:Optional[str]
#     event_id: Optional[int]




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






class Options(BaseModel):
    zero:Optional[str]
    one:Optional[str]



class Validators(BaseModel):
    email:Optional[str]
    maximum:Optional[str]
    maxLength:Optional[str]
    minimum:Optional[str]
    minLength:Optional[str]
    required:Optional[str]



class Fields(BaseModel):
    fieldName:Optional[str]
    fieldType:Optional[str]
    options:Optional[list[Options]] | None = None
    validators: Optional[list[Validators]] | None = None



class ParticipantFieldRequest(BaseModel):
    fields: Optional[list[Fields]] | None = None
    event_id:Optional[int]




    class Config:
        orm_mode = True




# class UpdateParticipantField(BaseModel):
#     id:Optional[int]
#     field_name:Optional[str]
#     field_type:Optional[str]
#     field_validation:Optional[str]
#     field_max_length:Optional[str]
#     field_min_length:Optional[str]
#     event_id:Optional[int]
