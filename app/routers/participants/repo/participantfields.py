from fastapi import status, Form
from routers.participants.schemas import participants
from models.models import Participant, ParticipantFields, Event
from utils.database import Database
from fastapi.exceptions import HTTPException
from passlib.context import CryptContext
from mail import sendmail
from fastapi.responses import FileResponse





database = Database()
engine = database.get_db_connection()
session = database.get_db_session(engine)


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")









# PARTICIPANT FIELDS CRUD ENDPOINT



async def add_participant_fields(participantFieldRequest: participants.ParticipantFieldRequest):

    new_participant_field = ParticipantFields()
    new_participant_field.field_name = participantFieldRequest.field_name
    new_participant_field.field_type = participantFieldRequest.field_type
    new_participant_field.field_validation = participantFieldRequest.field_validation
    new_participant_field.field_max_length = participantFieldRequest.field_max_length
    new_participant_field.field_min_length = participantFieldRequest.field_min_length
    new_participant_field.event_id = participantFieldRequest.event_id
    new_participant_field.status = 1
    
    session.add(new_participant_field)
    session.flush()
    session.refresh(new_participant_field, attribute_names=['id'])
    data = {
        "field_name": new_participant_field.field_name,
        "field_type": new_participant_field.field_type,
        "field_validation": new_participant_field.field_validation,
        "field_max_length": new_participant_field.field_max_length,
        "field_min_length": new_participant_field.field_min_length,
        "event_id": new_participant_field.event_id
    }
    session.commit()
    session.close()
    return data



from sqlalchemy import and_, desc




async def all_Participant_Fields():
    data = session.query(ParticipantFields).all()
    return data






from utils.config import settings



async def get_Participant_Fields_By_Id(event_id: int):
    

    participantFields_data = session.query(ParticipantFields).filter(
         ParticipantFields.event_id == event_id).first()
    
    if not participantFields_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Event with the id {event_id} is not available under ParticipantFields")
    data = session.query(Event).filter(Event.id == event_id).first()
    flyer_path = f"{settings.flyer_upload_dir}/{data.flyer}"
    program_outline_path = f"{settings.program_outline_upload_dir}/{data.program_outline}"

    db_data = {
        "event_name": data.event_name,
        "flyer": flyer_path,
        "program_outline": program_outline_path,
        "field_name": participantFields_data.field_name,
        "field_type": participantFields_data.field_type,
        "field_validation": participantFields_data.field_validation,
        "field_max_length": participantFields_data.field_max_length,
        "field_min_length": participantFields_data.field_min_length
    }
    return db_data
    









async def get_Participant_Fields_By_Event_Name(event_name: str):
    participantFields_data = session.query(ParticipantFields).filter(
         ParticipantFields.event_id == Event.id, Event.event_name == event_name).first()
    
    if not participantFields_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Event name {event_name} is not available under ParticipantFields")
    data = session.query(Event).filter(Event.event_name == event_name).first()
    flyer_path = f"{settings.flyer_upload_dir}/{data.flyer}"
    program_outline_path = f"{settings.program_outline_upload_dir}/{data.program_outline}"

    db_data = {
        "event_name": data.event_name,
        "flyer": flyer_path,
        "program_outline": program_outline_path,
        "field_name": participantFields_data.field_name,
        "field_type": participantFields_data.field_type,
        "field_validation": participantFields_data.field_validation,
        "field_max_length": participantFields_data.field_max_length,
        "field_min_length": participantFields_data.field_min_length
    }
    return db_data