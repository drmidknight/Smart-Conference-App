from routers.events.schemas.events import EventRequest, UpdateEventRequest
from fastapi import APIRouter,Depends, File, UploadFile, Form
from routers.events.schemas import events
from passlib.context import CryptContext
from routers.events.repo import crud
from utils.database import Database
from auth import authentication
from models.models import Admin
from sqlalchemy import text
from typing import Optional








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
                description:str = Form(None), flyer: Optional[UploadFile] = File(None),
                program_outline: Optional[UploadFile] = File(None),
                #current_admin: Admin = Depends(authentication.get_current_user)
                ):
        
    return await crud.add_event(
        event_name,venue,start_date,end_date,
        registration_time,how_to_join,number_of_participants,
        description,flyer,program_outline
    )
















@events_router.get("/all")
async def all_event():
    
    return await crud.all_event()






@events_router.get("/id/{id}")
async def get_event_by_id(id: str):
    
    return await crud.getEventById(id)










@events_router.put("/update")
async def update_Event(updateEvent: events.UpdateEventRequest):
    
    return await crud.update_Event(updateEvent)








@events_router.get("/name/{event_name}")
async def get_event_by_name(event_name: str):
    
    return await crud.getEventByName(event_name)











@events_router.delete("/delete/{id}")
async def deleteEvent(id: int):
    
    return await crud.deleteEvent(id)






@events_router.get("/event_url/{event_name}")
async def generate_url(event_name: str):
    
    return await crud.generate_url(event_name)







@events_router.get("/count")
async def count_all_Event():
    
    return await crud.count_all_Event()










@events_router.put("/upload")
async def add_only_flies(event_id: int, flyer: UploadFile = File(None), program_outline: UploadFile = File(None)):
    
    return await crud.add_only_flyer(event_id,flyer,program_outline)


















# from utils.config import settings



# @events_router.get("/getflyerEventById/{id}")
# async def get_flyer_Event_By_Id(id: str):
    
#     return crud.get_flyer_Event_By_Id(id)






# @events_router.get("/getflyerByEventByName/{event_name}")
# async def get_flyer_By_Event_By_Name(event_name: str):
#     data = session.query(Event).filter(Event.event_name == event_name).first()

#     dirname = os.path.join(os.getcwd(), "flyer")

#     eventByNamefileResponse = FileResponse(f"{dirname}/{data.flyer}")

#     if data or eventByNamefileResponse is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f"Event flyer does not exist")
    
#     return eventByNamefileResponse







# # from fastapi.responses import FileResponse

# @events_router.get("/read_image")
# async def read_image():
#     #dirname = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__))))
#     dirname = os.path.join(os.getcwd(), "flyer")

#     return FileResponse(f"{dirname}/EID AL-ADHA.png")

# #     #return FileResponse("app/flyers/FEMITECH.jpg")





