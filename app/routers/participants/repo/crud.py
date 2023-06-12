from fastapi import status, Form
from app.routers.participants.schemas import participants
from app.models.models import Event,Participant, ParticipantFields
from app.utils.database import Database
from fastapi.exceptions import HTTPException
from passlib.context import CryptContext
from app.mail import sendmail
from fastapi.responses import FileResponse





database = Database()
engine = database.get_db_connection()
session = database.get_db_session(engine)


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


IMAGEDIR = "app/flyers"




async def read_flyer(event_id: int):
    event_data = session.query(Event).filter(Event.id == event_id).first()
    db_flyer_name = f'app/flyers/{event_data.flyer}'
    return FileResponse(db_flyer_name)



async def add_participants(name:str = Form(...), phone_number:str = Form(...),
                gender:str = Form(None), email:str = Form(...),
                registration_time:str = Form(None) ,organization:str = Form(None),
                  how_to_join:str = Form(None), location:str = Form(None),
                  event_id:int = Form(None)):

    email_query = session.query(Participant).filter(
        Participant.email == email).first()
    
    phone_query = session.query(Participant).filter(
        Participant.phone_number == phone_number).first()

    if email_query or phone_query:
        raise HTTPException(status_code=status.HTTP_303_SEE_OTHER,
           detail=f"Participant with email or phone number already exists")


    new_participant = Participant()
    new_participant.name = name
    new_participant.phone_number = phone_number
    new_participant.gender = gender
    new_participant.email = email
    new_participant.organization = organization
    new_participant.how_to_join = how_to_join
    new_participant.registration_time = registration_time
    new_participant.location = location
    new_participant.event_id = event_id
    new_participant.status = 0
    
    session.add(new_participant)
    session.flush()
    session.refresh(new_participant, attribute_names=['id'])

    event_data = session.query(Event).filter(Event.id == event_id).first()
    read_flyer_image = read_flyer(event_id)
    #db_flyer_name = f'app/flyers/{event_data.flyer}'

    await sendmail.sendEmailToNewParticipant([new_participant.email], new_participant, read_flyer_image)
    data = {
        "phone_number": new_participant.phone_number,
        "email": new_participant.email,
        "status": new_participant.status,
        "registration_time": new_participant.registration_time,
        "event_id": new_participant.event_id,
        "gender": new_participant.gender,
        "name": new_participant.name,
        "organization": new_participant.organization,
        "attend_by": new_participant.how_to_join,
        "location": new_participant.location
    }
    session.commit()
    session.close()
    return data






async def all_Participant():
    data = session.query(Participant).all()
    return data






async def get_Participant_By_Id(id: int):
    data = session.query(Participant).filter(Participant.id == id).all()
    
    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Participant with the id (" + str(id) + ") is not found")
    return data
    









async def updateParticipant(updateParticipant: participants.UpdateParticipant):
    participant_id = updateParticipant.id
    is_Participant_update = session.query(Participant).filter(Participant.id == participant_id).update({
            Participant.name: updateParticipant.name,
            Participant.phone_number: updateParticipant.phone_number,
            Participant.gender: updateParticipant.gender,
            Participant.email: updateParticipant.email,
            Participant.organization: updateParticipant.organization,
            Participant.attend_by: updateParticipant.attend_by,
            Participant.registration_time: updateParticipant.registration_time,
            Participant.location: updateParticipant.location,
            Participant.event_id: updateParticipant.event_id,
            Participant.status: 1
        }, synchronize_session=False)
    session.flush()
    session.commit()
    if not is_Participant_update:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Participant with the id (" + str(participant_id) + ") is not found")

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





    






async def get_Participant_By_attend_by(attend_by: str):
    data = session.query(Participant).filter(
            Participant.attend_by == attend_by).all()
    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Attend by (" + str(attend_by) + ") is not available")
    elif attend_by == "virtual":
            data = session.query(Participant).filter(Participant.attend_by == attend_by).all()
    elif attend_by == "onsite":
            data = session.query(Participant).filter(Participant.attend_by == attend_by).all()
    return data









async def deleteParticipant(id: str):
    db_data = session.query(Participant).filter(Participant.id == id).update({
            Participant.status: 0
            }, synchronize_session=False)
    session.flush()
    session.commit()
    if not db_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Participant with the id (" + str(id) + ") is not available")

    data = session.query(Participant).filter(Participant.id == id).one()
    return data








async def show_participant_event_all(id: int):
    data = session.query(Participant).filter(
            Participant.event_id == Event.id).filter(Event.id == id).all()
    
    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Participant with the id {id} is not available")
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




















# PARTICIPANT FIELDS CRUD ENDPOINT



async def add_participant_fields(field_name:str = Form(...), field_type:str = Form(...),
                field_validation:int = Form(None), field_max_length:int = Form(None),
                field_min_length:int = Form(None) ,event_id:int = Form(...) ):

    new_participant_field = ParticipantFields()
    new_participant_field.field_name = field_name
    new_participant_field.field_type = field_type
    new_participant_field.field_validation = field_validation
    new_participant_field.field_max_length = field_max_length
    new_participant_field.field_min_length = field_min_length
    new_participant_field.event_id = event_id
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








async def all_Participant_Fields():
    data = session.query(ParticipantFields).all()
    return data





async def get_Participant_Fields_By_Id(id: int):
    data = session.query(ParticipantFields).filter(ParticipantFields.event_id == id).all()
    
    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"ParticipantFields with the id (" + str(id) + ") is not found")
    return data