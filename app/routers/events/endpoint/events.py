from fastapi import APIRouter, status, Depends, File, UploadFile, Form
from routers.events.schemas import events
from models.models import Admin, Event
from utils.database import Database
from auth import authentication
from fastapi.exceptions import HTTPException
from passlib.context import CryptContext
import shutil
from response.response import Response
from routers.events.repo import crud
from fastapi.responses import FileResponse
from sqlalchemy import text
import os
from routers.events.schemas.events import EventRequest, UpdateEventRequest
from typing import Optional, List



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



# @events_router.post("/addEventWithOutFile", response_description="Event data added into the database")
# async def add_event_without_file(eventRequest: EventRequest,
#                     #flyer: Optional[UploadFile] = File(None),program_outline: Optional[UploadFile] = File(None),
#                  #current_admin: Admin = Depends(authentication.get_current_user)
#                 ):
    
#     return await crud.add_event(eventRequest)







@events_router.post("/addEventWithFile", response_description="Event data added into the database")
async def add_event(event_name:str = Form(...), venue:str = Form(...),
                start_date:str = Form(...), end_date:str = Form(...),
                registration_time:str = Form(None) ,how_to_join:str = Form(None),
                  number_of_participants:str = Form(None),
                description:str = Form(None), flyer: Optional[UploadFile] = File(None),
                program_outline: Optional[UploadFile] = File(None),
                #current_admin: Admin = Depends(authentication.get_current_user)
                ):
        
    return await crud.add_event_with_files(
        event_name,venue,start_date,end_date,
        registration_time,how_to_join,number_of_participants,
        description,flyer,program_outline
    )


# async def add_event(event_name:str, venue:str,
#                 start_date:str, end_date:str,
#                 registration_time:str ,how_to_join:str,
#                   number_of_participants:str,
#                 description:str, flyer: UploadFile = File(None),
#                 program_outline: UploadFile = File(None),
#                 #current_admin: Admin = Depends(authentication.get_current_user)
#                 ):
    
#     return await crud.add_event(
#         event_name,venue,start_date,end_date,
#         registration_time,how_to_join,number_of_participants,
#         description,flyer,program_outline
#     )













# async def add_event(addEvent: EventRequest,
#                 program_outline: UploadFile = File(None), flyer: UploadFile = File(None),
#                 current_admin: Admin = Depends(authentication.get_current_user)):
    
#     admin_id = current_admin.id

#     db_query = session.query(Event).filter(
#             Event.event_name == addEvent.event_name
#         ).first()

#     if db_query is not None:
#         raise HTTPException(status_code=status.HTTP_303_SEE_OTHER,
#            detail=f"Event (" + \
#         str(addEvent.event_name) + ") already exists")

#     flyer_name:str = flyer.filename

#     program_outline_name:str = program_outline.filename


#     new_event = Event(
#     event_name = addEvent.event_name,
#     venue = addEvent.venue,
#     start_date = addEvent.start_date,
#     end_date = addEvent.end_date,
#     how_to_join = addEvent.how_to_join,
#     registration_time = addEvent.registration_time,
#     number_of_participants = addEvent.number_of_participants,
#     description = addEvent.description,
#     flyer = flyer_name,
#     program_outline = program_outline_name,
#     admin_id = admin_id,
#     status = "Active"
#     )
#     session.add(new_event)
#     # session.flush()
#     # session.refresh(new_event, attribute_names=['id'])
#     session.commit()
#     session.close()

#     # try:
#     #     flyer_contents = flyer.file.read()
#     #     with open(flyer.filename, 'wb') as f:
#     #         f.write(flyer_contents)
#     # except Exception:
#     #     return {"message": "There was an error uploading flyer"}
#     # finally:
#     #     flyer.file.close()


#     # try:
#     #     program_outline_contents = program_outline.file.read()
#     #     with open(program_outline.filename, 'wb') as f:
#     #         f.write(program_outline_contents)
#     # except Exception:
#     #     return {"message": "There was an error uploading program_outline"}
#     # finally:
#     #     program_outline.file.close()
        
#     return new_event




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










@events_router.put("/uploadFiles")
async def add_only_flyer(event_id: int, flyer: UploadFile = File(None), program_outline: UploadFile = File(None)):
    
    return await crud.add_only_flyer(event_id,flyer,program_outline)








from utils.config import settings

# @events_router.post("/uploader")
# async def add_only_files(flyer: Optional[UploadFile] = File(None), program_outline: Optional[UploadFile] = File(None)):

#     flyer_name = f"flyer-" + str("event_name") + ".jpg"
#     program_outline_name = f"program_outline-" + str("event_name") + ".pdf"

#        # get flyer destination path
#     flyer_dest = os.path.join(settings.flyer_upload_dir, flyer_name)
#     print(flyer_dest)


#        # get program_outline destination path
#     program_outline_dest = os.path.join(settings.program_outline_upload_dir, program_outline_name)
#     print(program_outline_dest)



#     try:
#         flyer_contents = flyer.file.read()
#         with open(flyer_dest, 'wb') as f:
#             f.write(flyer_contents)
#     except Exception:
#         return {"message": "There was an error uploading flyer"}
#     finally:
#         flyer_name


#     try:
#         program_outline_contents = program_outline.file.read()
#         with open(program_outline_dest, 'wb') as f:
#             f.write(program_outline_contents)
#     except Exception:
#         return {"message": "There was an error uploading program_outline"}
#     finally:
#         program_outline_name


#     return {"message": "files uploaded successfully"}






@events_router.get("/getflyerEventById/{id}")
async def get_flyer_Event_By_Id(id: str):
    data = session.query(Event).filter(Event.id == id).first()

    dirname = os.path.join(os.getcwd(), "flyer")

    fileResponse = FileResponse(f"{dirname}/{data.flyer}")

    if not data or fileResponse:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Event flyer does not exist")
    
    return fileResponse











@events_router.get("/getflyerByEventByName/{event_name}")
async def get_flyer_By_Event_By_Name(event_name: str):
    data = session.query(Event).filter(Event.event_name == event_name).first()

    dirname = os.path.join(os.getcwd(), "flyer")

    fileResponse = FileResponse(f"{dirname}/{data.flyer}")

    if not data or fileResponse:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Event flyer does not exist")
    
    return fileResponse









# from fastapi.responses import FileResponse

@events_router.get("/read_image")
async def read_image():
    #dirname = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__))))
    dirname = os.path.join(os.getcwd(), "flyer")

    return FileResponse(f"{dirname}/EID AL-ADHA.png")

#     #return FileResponse("app/flyers/FEMITECH.jpg")





