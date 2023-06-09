from fastapi import APIRouter, Form
from app.routers.participants.schemas import participants
from app.routers.events.models.models import Event
from app.routers.participants.models.models import Participant
from app.utils.database import Database
from passlib.context import CryptContext
from app.mail import sendmail
from app.routers.participants.repo import crud


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
async def create_participants(name:str = Form(...), phone_number:str = Form(...),
                gender:str = Form(None), email:str = Form(...),
                registration_time:str = Form(None) ,organization:str = Form(None),
                  how_to_join:str = Form(None), location:str = Form(None),
                  event_id:int = Form(None)):

    return await crud.add_participants(name,phone_number,gender,email,registration_time,
                                       organization,how_to_join,location,event_id)





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

















# # PARTICIPANT FIELDS CRUD ENDPOINT

@router.post("/addParticipantFields", response_description="Participant Field data added into the database")
async def create_participants_Fields(field_name:str = Form(...), field_type:str = Form(...),
                field_validation:int = Form(None), field_max_length:int = Form(None),
                field_min_length:int = Form(None) ,event_id:int = Form(...)):

    return await crud.add_participant_fields(field_name,field_type,field_validation,
                                             field_max_length,field_min_length,event_id)





@router.get("/getAllParticipantFields")
async def all_Participant_Fields():

    return await crud.all_Participant_Fields()









@router.get("/getParticipantFieldById/{id}")
async def get_Participant_Fields_By_Id(id: int):
    
    return await crud.get_Participant_Fields_By_Id(id)