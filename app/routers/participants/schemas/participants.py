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
    zero:Optional[str] | None = None
    one:Optional[str] | None = None



class Validators(BaseModel):
    email:Optional[str] | None = None
    maximum:Optional[int] | None = None
    maxLength:Optional[int] | None = None
    minimum:Optional[int] | None = None
    minLength:Optional[int] | None = None
    required:Optional[str] | None = None



class Fields(BaseModel):
    fieldName:Optional[str] | None = None
    fieldType:Optional[str] | None = None
    options:Optional[list[Options]] | None = None
    validators: Optional[list[Validators]] | None = None



class ParticipantFieldRequest(BaseModel):
    fields: Optional[list[Fields]] | None = None
    event_id:Optional[int]




    class Config:
        orm_mode = True,
        schema_extra = {
            "fields": [
                {
                    "fieldName": "name",
                    "fieldType": "textField",
                    "options": [
                        {
                            "zero": "",
                            "one": ""
                        }
                    ],
                    "validators": [
                        {
                            "email": "",
                            "maximum": "",
                            "maxLength": "50",
                            "minimum": "",
                            "minLength": "3",
                            "required": "true"
                        }
                    ]
                },

                {
                    "fieldName": "gender",
                    "fieldType": "dropdown",
                    "options": [
                        {
                            "zero": "male",
                            "one": "female"
                        }
                    ],
                    "validators": [
                        {
                            "email": "",
                            "maximum": "",
                            "maxLength": "",
                            "minimum": "",
                            "minLength": "",
                            "required": "true"
                        }
                    ]
                },

                {
                    "fieldName": "email",
                    "fieldType": "textField",
                    "options": [
                        {
                            "zero": "",
                            "one": ""
                        }
                    ],
                    "validators": [
                        {
                            "email": "",
                            "maximum": "",
                            "maxLength": "50",
                            "minimum": "",
                            "minLength": "3",
                            "required": "true"
                        }
                    ]
                }
            ]
        }













# class UpdateParticipantField(BaseModel):
#     id:Optional[int]
#     field_name:Optional[str]
#     field_type:Optional[str]
#     field_validation:Optional[str]
#     field_max_length:Optional[str]
#     field_min_length:Optional[str]
#     event_id:Optional[int]
