from fastapi import status, Form
from routers.participants.schemas import participants
from models.models import Participant, ParticipantFields, Event
from utils.database import Database
from fastapi.exceptions import HTTPException
from passlib.context import CryptContext
from mail import sendmail
from fastapi.responses import FileResponse
import json
from fastapi.encoders import jsonable_encoder
from typing import Any, Optional




database = Database()
engine = database.get_db_connection()
session = database.get_db_session(engine)


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


IMAGEDIR = "app/flyers"




async def read_flyer(event_id: int):
    event_data = session.query(Event).filter(Event.id == event_id).first()
    db_flyer_name = f'app/flyers/{event_data.flyer}'
    return FileResponse(db_flyer_name)



async def add_participants(participantRequest: participants.ParticipantRequest):


    new_participant = Participant()
    new_participant.form_values = json.dumps(participantRequest.form_values)
    new_participant.event_id = participantRequest.event_id
    new_participant.status = 0
    
    session.add(new_participant)
    session.flush()
    session.refresh(new_participant, attribute_names=['id'])
    session.commit()
    session.close()
    return new_participant






async def all_Participant():
    data = session.query(Participant).all()
    return data






async def get_Participant_By_Id(id: int):
    data = session.query(Participant).filter(Participant.id == id).all()
    
    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Participant with the id (" + str(id) + ") is not found")
    return data
    









async def updateParticipant(updateParticipant: participants.UpdateParticipant):
    participant_id = updateParticipant.id
    is_Participant_update = session.query(Participant).filter(Participant.id == participant_id).update({
            Participant.name: updateParticipant.name,
            Participant.phone_number: updateParticipant.phone_number,
            Participant.gender: updateParticipant.gender,
            Participant.email: updateParticipant.email,
            Participant.organization: updateParticipant.organization,
            Participant.how_to_join: updateParticipant.how_to_join,
            Participant.registration_time: updateParticipant.registration_time,
            Participant.location: updateParticipant.location,
            Participant.event_id: updateParticipant.event_id,
            Participant.status: 1
        }, synchronize_session=False)
    session.flush()
    session.commit()
    if not is_Participant_update:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail="Participant with the id (" + str(participant_id) + ") is not found")

    data = session.query(Participant).filter(Participant.id == participant_id).one()
    return data











async def phone_number_email(phone_number_email: str):
    if "@" in phone_number_email:
        participant = session.query(Participant).filter(
            Participant.email == phone_number_email).first()
    else:
        participant = session.query(Participant).filter(
            Participant.phone_number == phone_number_email).first()
    return participant





    






async def get_Participant_By_how_to_join(how_to_join: str):
    data = session.query(Participant).filter(
            Participant.how_to_join == how_to_join).all()
    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail="Attend by (" + str(how_to_join) + ") is not available")
    elif how_to_join == "virtual":
            data = session.query(Participant).filter(Participant.how_to_join == how_to_join).all()
    elif how_to_join == "onsite":
            data = session.query(Participant).filter(Participant.how_to_join == how_to_join).all()
    return data









async def deleteParticipant(id: str):
    db_data = session.query(Participant).filter(Participant.id == id).update({
            Participant.status: 0
            }, synchronize_session=False)
    session.flush()
    session.commit()
    if not db_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail="Participant with the id (" + str(id) + ") is not available")

    data = session.query(Participant).filter(Participant.id == id).one()
    return data








async def show_participant_event_all(id: int):
    data = session.query(Participant).filter(
            Participant.event_id == Event.id).filter(Event.id == id).all()
    
    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Participant with the id {id} is not available")
    return data









async def count_all_Participant():
    data = session.query(Participant).count()
    return data






async def count_all_Participant_Confirm():
    data = session.query(Participant).filter(Participant.status == 1).count()
    return data







async def count_all_Participant_Not_Confirm():
    data = session.query(Participant).filter(Participant.status == 0).count()
    return data







async def get_Participants_By_Event_ID(event_id: int)-> Any:

    data = session.query(Participant).filter(
        Participant.event_id == event_id).all()

    
    
    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Event with the id (" + str(event_id) + ") is not found")

    # flyer_path = f"{settings.flyer_upload_dir}/{data.flyer}"
    # program_outline_path = f"{settings.program_outline_upload_dir}/{data.program_outline}"
    event_data = session.query(Event).filter(Event.id == event_id).first()
    # full_data = {
    #     "event_name": event_data.event_name,
    #     "flyer": flyer_path,
    #     "program_outline": program_outline_path,
    #     "field_name": data.fields
    # }

    fields_con: Any = data

    fields = json.loads(fields_con.form_values)
   
    db_data = {
        "id": data.id,
        "event_id": data.event_id,
        "event_name": event_data.event_name,
        "form_values": [fields]
        
    }
       
    return  jsonable_encoder([db_data])
