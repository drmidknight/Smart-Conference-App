from fastapi import APIRouter, Form, File, UploadFile,status
from routers.participants.schemas import participants
from routers.events.models.models import Event
from routers.participants.models.models import Participant
from utils.database import Database
from passlib.context import CryptContext
from routers.participants.repo import participantfields
from fastapi.responses import FileResponse
from fastapi.exceptions import HTTPException
from typing import Optional, List, Any



# APIRouter creates path operations for Participant Fields module
participantfields_router = APIRouter(
    prefix="/participantfields",
    tags=["Participant Fields"],
    responses={404: {"description": "Not found"}},
)




database = Database()
engine = database.get_db_connection()
session = database.get_db_session(engine)








# # PARTICIPANT FIELDS CRUD ENDPOINT

@participantfields_router.post("/addParticipantFields",  response_description="Participant Field data added into the database")
async def create_participants_Fields(participantFieldRequest: participants.ParticipantFieldRequest):

    return await participantfields.add_participant_fields(participantFieldRequest)





@participantfields_router.get("/getAllParticipantFields")
async def all_Participant_Fields()-> Any:

    return await participantfields.all_Participant_Fields()









@participantfields_router.get("/getParticipantFieldByEventId/{event_id}")
async def get_Participant_Fields_By_Event_Id(event_id: int):
    
    return await participantfields.get_Participant_Fields_By_Id(event_id)








import os
# @participantfields_router.get("/getflyerByEventId/{event_id}")
# async def get_flyer_By_Event_Id(event_id: str):
#     data = session.query(Event).filter(Event.id == event_id).first()

#     dirname = os.path.join(os.getcwd(), "flyer")

#     fileResponse = FileResponse(f"{dirname}/{data.flyer}")

#     if not data or fileResponse:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f"{data.event_name} event flyer does not exist")
    
#     return f"{dirname}/{data.flyer}"



# @participantfields_router.get("/getflyerByEventId/{event_id}")
# async def get_flyer_By_Event_Id(event_id: str):
#     data = session.query(Event).filter(Event.id == event_id).first()

#     dirname = os.path.join(os.getcwd(), "flyer")

#     fileResponse = FileResponse(f"{dirname}/{data.flyer}")

#     if not data or fileResponse:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f"{data.event_name} event flyer does not exist")
    
#     return FileResponse(f"{dirname}/{data.flyer}")








@participantfields_router.get("/getParticipantFieldByEventName/{event_name}")
async def get_Participant_Fields_By_Event_Name(event_name: str):
    
    return await participantfields.get_Participant_Fields_By_Event_Name(event_name)





# @participantfields_router.get("/getflyerByEventName/{event_name}")
# async def getflyerByEventName(event_name: str):
#     data = session.query(Event).filter(Event.event_name == event_name).first()

#     dirname = os.path.join(os.getcwd(), "flyer")

#     fileResponse = FileResponse(f"{dirname}/{data.flyer}")

#     if not data or fileResponse:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f"{data.event_name} event flyer does not exist")
    
#     return FileResponse(f"{dirname}/{data.flyer}")
