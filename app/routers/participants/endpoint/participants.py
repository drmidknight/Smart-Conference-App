from fastapi import APIRouter, status
from routers.participants.schemas import participants
from routers.events.models.models import Event
from routers.participants.models.models import Participant
from utils.database import Database
from passlib.context import CryptContext
from mail import sendmail
from routers.participants.repo import crud


# APIRouter creates path operations for staffs module
router = APIRouter(
    prefix="/participant",
    tags=["Participant"],
    responses={404: {"description": "Not found"}},
)




database = Database()
engine = database.get_db_connection()
session = database.get_db_session(engine)


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")






# PARTICIPANT FIELDS CRUD ENDPOINT

@router.post("/add", response_description="Participant data added into the database")
async def create_participants(participantRequest: participants.ParticipantRequest):

    return await crud.add_participants(participantRequest)





@router.get("/getAllParticipant")
async def all_Participant():

    return await crud.all_Participant()





@router.get("/getParticipantById/{id}")
async def get_Participant_By_Id(id: int):
    
    return await crud.get_Participant_By_Id(id)
    








@router.put("/update")
async def updateParticipant(updateParticipant: participants.UpdateParticipant):
    
    return await crud.updateParticipant(updateParticipant)










@router.get("/phone_number_email/{phone_number_email}")
async def phone_number_email(phone_number_email: str):
    
    return await crud.phone_number_email(phone_number_email)




    





@router.get("/attend_program_by/{attend_by}")
async def get_Participant_By_attend_by(attend_by: str):
    
    return await crud.get_Participant_By_attend_by(attend_by)








@router.delete("/delete/{id}")
async def deleteParticipant(id: str):
    
    return await crud.deleteParticipant(id)







@router.get("/participant_event/{id}")
async def show_participant_event_all(id: int):
    
    return await crud.show_participant_event_all(id)









@router.get("/countParticipant")
async def count_all_Participant():
    
    return await crud.count_all_Participant()





@router.get("/countParticipantConfirm")
async def count_all_Participant_Confirm():
    
    return await crud.count_all_Participant_Confirm()





@router.get("/countParticipantNotConfirm")
async def count_all_Participant_Not_Confirm():
    
    return await crud.count_all_Participant_Not_Confirm()



















# PARTICIPANT FIELDS CRUD ENDPOINT

@router.post("/addParticipantFields", response_description="Participant Field data added into the database")
async def create_participants(participantFieldRequest: participants.ParticipantFieldRequest):

    return await crud.add_participant_fields(participantFieldRequest)





@router.get("/getAllParticipantFields")
async def all_Participant_Fields():

    return await crud.all_Participant_Fields()