from fastapi import status, Form, Request
from routers.participants.schemas import participants
from models.models import Participant, ParticipantFields, Event
from utils.database import Database
from fastapi.exceptions import HTTPException
from passlib.context import CryptContext
from mail import sendmail
from fastapi.responses import FileResponse
import json
from typing import Any, Optional
from fastapi.encoders import jsonable_encoder




database = Database()
engine = database.get_db_connection()
session = database.get_db_session(engine)


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")









# PARTICIPANT FIELDS CRUD ENDPOINT

async def add_participant_fields(participantFieldRequest: participants.ParticipantFieldRequest):
    
    db_query = session.query(ParticipantFields).filter(
            ParticipantFields.event_id == participantFieldRequest.event_id
        ).first()

    if db_query is not None:
        raise HTTPException(status_code=status.HTTP_303_SEE_OTHER,
           detail="Event (" + \
        str(participantFieldRequest.event_id) + ") already exists")
    
    json_data = jsonable_encoder({key: item for key, item in enumerate(participantFieldRequest.fields)})

    #json_data = jsonable_encoder({key.replace('"', ''): item for key, item in enumerate(participantFieldRequest.fields)})
    
    new_participant_field = ParticipantFields()
    new_participant_field.fields = json.dumps(json_data)
    new_participant_field.event_id = participantFieldRequest.event_id
    new_participant_field.status = 1
    
    session.add(new_participant_field)
    session.flush()
    session.refresh(new_participant_field, attribute_names=['id'])
    data = {
        "field_name": new_participant_field.fields,
        "event_id": new_participant_field.event_id
    }
    session.commit()
    session.close() 
    return data







async def all_Participant_Fields()-> Any:
    data = session.query(ParticipantFields).all()

    fields = json.loads(data.fields)

    db_data = {
        "id": data.id,
        "event_id": data.event_id,
        "fields": [fields]
    }
       
    return  jsonable_encoder(db_data)






from utils.config import settings


async def get_Participant_Fields_By_Id(event_id: int)-> Any:

    data = session.query(ParticipantFields).filter(
        ParticipantFields.event_id == event_id).first()

    #event_data = session.query(Event).filter(Event.id == event_id).first()
    
    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Event with the id (" + str(event_id) + ") is not found")

    # flyer_path = f"{settings.flyer_upload_dir}/{data.flyer}"
    # program_outline_path = f"{settings.program_outline_upload_dir}/{data.program_outline}"

    # full_data = {
    #     "event_name": event_data.event_name,
    #     "flyer": flyer_path,
    #     "program_outline": program_outline_path,
    #     "field_name": data.fields
    # }

    fields = json.loads(data.fields)
   
    db_data = {
        "fields": [fields],
        "event_id": data.event_id
    }
       
    return  jsonable_encoder(db_data)












async def get_Participant_Fields_By_Event_Name(event_name: str):
    data = session.query(ParticipantFields).filter(
        ParticipantFields.event_id == Event.id,
        Event.event_name == event_name
        ).first()

    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail= "Event (" + str(event_name) + ") is not found")

    fields = json.loads(data.fields)
   
    db_data = {
        "fields": [fields],
        "event_name": event_name
    }
       
    return  jsonable_encoder(db_data)



















# async def get_Participant_Fields_By_Event_Name(event_name: str):
#     data = session.query(ParticipantFields).filter(
#         ParticipantFields.event_id == Event.id,
#         Event.event_name == event_name
#         ).first()

#     #event_data = session.query(Event).filter(Event.event_name == event_name).first()

#     # flyer_path = f"{settings.flyer_upload_dir}/{data.flyer}"
#     # program_outline_path = f"{settings.program_outline_upload_dir}/{data.program_outline}"

#     if not data:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f"event (" + str(event_name) + ") is not found")

#     fields = json.loads(data.fields)
   
#     db_data = {
#         "fields": [fields],
#         "event_name": event_name
#     }
       
#     return  jsonable_encoder(db_data)