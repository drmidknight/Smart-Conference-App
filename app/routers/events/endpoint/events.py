from fastapi import APIRouter, status, Depends, File, UploadFile, Form
from app.routers.events.schemas import events
from app.models.models import Event, Admin
from app.utils.database import Database
from app.auth import authentication
from fastapi.exceptions import HTTPException
from passlib.context import CryptContext
import shutil
from app.response.response import Response
from app.routers.events.repo import crud



# APIRouter creates path operations for events module
events_router = APIRouter(
    prefix="/event",
    tags=["Event"],
    responses={404: {"description": "Not found"}},
)




database = Database()
engine = database.get_db_connection()
session = database.get_db_session(engine)


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")









@events_router.post("/add", response_description="Event data added into the database")
async def add_event(event_name:str = Form(...), venue:str = Form(...),
                start_date:str = Form(...), end_date:str = Form(...),
                registration_time:str = Form(None) ,how_to_join:str = Form(None),
                  number_of_participants:str = Form(None),
                description:str = Form(None), flyer: UploadFile = File(None),
                program_outline: UploadFile = File(None),
                current_admin: Admin = Depends(authentication.get_current_user)):
    
    return await crud.add_event(
        event_name,venue,start_date,end_date,
        registration_time,how_to_join,number_of_participants,
        description,flyer,program_outline,current_admin
    )









@events_router.get("/getAllEvents")
async def all_event():
    
    return await crud.all_event()






@events_router.get("/getEventById/{id}")
async def getEventById(id: str):
    
    return await crud.getEventById(id)










@events_router.put("/update")
async def update_Event(updateEvent: events.UpdateEventRequest):
    
    return await crud.update_Event(updateEvent)








@events_router.get("/getEventByName/{event_name}")
async def getEventByName(event_name: str):
    
    return await crud.getEventByName(event_name)











@events_router.delete("/delete/{id}")
async def deleteEvent(id: int):
    
    return await crud.deleteEvent(id)






@events_router.get("/event_url/{event_name}")
async def generate_url(event_name: str):
    
    return await crud.generate_url(event_name)





@events_router.get("/countEvent")
async def count_all_Event():
    
    return await crud.count_all_Event()










@events_router.put("/add_only_flyer")
async def add_only_flyer(event_id: int, flyer: UploadFile = File(None), program_outline: UploadFile = File(None)):
    
    return await crud.add_only_flyer(event_id,flyer,program_outline)














# from fastapi.responses import FileResponse

# @events_router.get("/read_image")
# async def read_image():
#     return FileResponse("app/other_docs/flyers/African Union Day.jpeg")

