from fastapi import APIRouter, status, Depends, File, UploadFile, Form
from routers.events.schemas.events import EventRequest, UpdateEventRequest
#from routers.admin.models.models import Admin
#from routers.events.models.models import Event
from models.models import Admin, Event
from utils.database import Database
from auth import authentication
from fastapi.exceptions import HTTPException
from passlib.context import CryptContext
import shutil
from response.response import Response
from routers.events.repo import crud
from fastapi.responses import FileResponse
import os



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

IMAGEDIR = "/"

# @events_router.post("post_image")
# def upload(flyer: UploadFile = File(None)):
#     try:
#         contents = flyer.file.read()
#         with open(flyer.filename, 'wb') as f:
#             f.write(contents)
#     except Exception:
#         return {"message": "There was an error uploading the file"}
#     finally:
#         flyer.file.close()

#     return {"message": f"Successfully uploaded {flyer.filename}"}




# @events_router.get("/read_image")
# async def read_image():
#     return FileResponse("AG.jpg")



# @events_router.post("/add", response_description="Event data added into the database")
# async def add_event(eventRequest: EventRequest,flyer: UploadFile = File(None),
#                  program_outline: UploadFile = File(None),
#                 current_admin: Admin = Depends(authentication.get_current_user)):
    
#     return await crud.add_event(eventRequest, flyer, program_outline, current_admin)



@events_router.post("/add", response_description="Event data added into the database")
async def add_event(addEvent: EventRequest,
                # program_outline: UploadFile = File(None), flyer: UploadFile = File(None),
                current_admin: Admin = Depends(authentication.get_current_user)):
    
    admin_id = current_admin.id

    db_query = session.query(Event).filter(
            Event.event_name == addEvent.event_name
        ).first()

    if db_query is not None:
        raise HTTPException(status_code=status.HTTP_303_SEE_OTHER,
           detail=f"Event (" + \
        str(addEvent.event_name) + ") already exists")

    #flyer_name:str = flyer.filename

    #program_outline_name:str = program_outline.filename


    new_event = Event()
    new_event.event_name = addEvent.event_name
    new_event.venue = addEvent.venue
    new_event.start_date = addEvent.start_date
    new_event.end_date = addEvent.end_date
    new_event.how_to_join = addEvent.how_to_join
    new_event.registration_time = addEvent.registration_time
    new_event.number_of_participants = addEvent.number_of_participants
    new_event.description = addEvent.description
    new_event.flyer = "flyer_name"
    new_event.program_outline = "program_outline_name"
    new_event.admin_id = admin_id
    new_event.status = "Active"
    
    session.add(new_event)
    # session.flush()
    # session.refresh(new_event, attribute_names=['id'])
    session.commit()
    session.close()

    # try:
    #     flyer_contents = flyer.file.read()
    #     with open(flyer.filename, 'wb') as f:
    #         f.write(flyer_contents)
    # except Exception:
    #     return {"message": "There was an error uploading flyer"}
    # finally:
    #     flyer.file.close()


    # try:
    #     program_outline_contents = program_outline.file.read()
    #     with open(program_outline.filename, 'wb') as f:
    #         f.write(program_outline_contents)
    # except Exception:
    #     return {"message": "There was an error uploading program_outline"}
    # finally:
    #     program_outline.file.close()
        
    return new_event




@events_router.get("/getAllEvents")
async def all_event():
    
    return await crud.all_event()






@events_router.get("/getEventById/{id}")
async def getEventById(id: str):
    
    return await crud.getEventById(id)










@events_router.put("/update")
async def update_Event(updateEvent: UpdateEventRequest):
    
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

