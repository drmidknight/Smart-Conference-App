from fastapi import APIRouter, status, Depends, File, UploadFile, Form
from routers.events.schemas import events
from models.models import Admin, Event
from utils.database import Database
from auth import authentication
from fastapi.exceptions import HTTPException
from passlib.context import CryptContext
import shutil
from response.response import Response
from fastapi.responses import FileResponse




IMAGEDIR = "app/flyers/"

PROGRAMOUTLINEDIR = "app/program_outlines/"




database = Database()
engine = database.get_db_connection()
session = database.get_db_session(engine)


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")










async def add_event(event_name:str = Form(...), venue:str = Form(...),
                start_date:str = Form(...), end_date:str = Form(...),
                registration_time:str = Form(None) ,how_to_join:str = Form(None),
                  number_of_participants:str = Form(None),
                description:str = Form(None),
                current_admin: Admin = Depends(authentication.get_current_user)):
    
    admin_id = current_admin.id

    db_query = session.query(Event).filter(
            Event.event_name == event_name
        ).first()

    if db_query is not None:
        raise HTTPException(status_code=status.HTTP_303_SEE_OTHER,
           detail=f"Event (" + \
        str(event_name) + ") already exists")

    #flyer_name:str = flyer.filename
    #program_outline_name:str = program_outline.filename

    new_event = Event()
    new_event.event_name = event_name
    new_event.venue = venue
    #new_event.flyer = flyer_name
    #new_event.program_outline = program_outline_name
    new_event.start_date = start_date
    new_event.end_date = end_date
    new_event.how_to_join = how_to_join
    new_event.registration_time = registration_time
    new_event.number_of_participants = number_of_participants
    new_event.description = description
    new_event.admin_id = admin_id
    new_event.status = "Active"
    
    session.add(new_event)
    session.flush()
    session.refresh(new_event, attribute_names=['id'])
    data = {
        "event_name": new_event.event_name,
        "venue": new_event.venue,
        "status": new_event.status,
        "flyer": new_event.flyer,
        "start_date": new_event.start_date,
        "end_date": new_event.end_date,
        "admin_id": new_event.admin_id,
        "registration_time": new_event.registration_time,
        "number_of_participants": new_event.number_of_participants,
        "description": new_event.description
    }
    session.commit()
    session.close()
    return data









async def all_event():
    data = session.query(Event).filter(Event.status == "Active").all()
    return data







async def getEventById(id: str):
    data = session.query(Event).filter(Event.id == id).all()
    
    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Event with the id {id} is not available")
    return data











async def update_Event(updateEvent: events.UpdateEventRequest):
    eventID = updateEvent.id
    is_eventID_update = session.query(Event).filter(Event.id == eventID).update({
            Event.event_name: updateEvent.event_name,
            Event.venue: updateEvent.venue,
            Event.start_date: updateEvent.start_date,
            Event.end_date: updateEvent.end_date,
            Event.registration_time: updateEvent.registration_time,
            Event.number_of_participants: updateEvent.number_of_participants,
            Event.description: updateEvent.description,
            Event.status: "Active"
        }, synchronize_session=False)
    session.flush()
    session.commit()
    if not is_eventID_update:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Event with the id (" + str(eventID) + ") is not available")

    data = session.query(Event).filter(Event.id == eventID).one()
    return data









async def getEventByName(event_name: str):
    data = session.query(Event).filter(Event.event_name == event_name).all()
    
    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Event with the event_name (" + str(event_name) + ") not found")
    return data












async def deleteEvent(id: int):
    db_data = session.query(Event).filter(Event.id == id).update({
            Event.status: "InActive"
            }, synchronize_session=False)
    session.flush()
    session.commit()
    if not db_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Event with the id (" + str(id) + ") is not available")

    data = session.query(Event).filter(Event.id == id).one()
    return data


async def generate_url(event_name: str):
    data = session.query(Event).filter(Event.event_name == event_name).first()
    
    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Event with the event_name (" + str(event_name) + ") not found")
                            
    db_event_name = data.event_name
    event_url = f"http://localhost:4200/" + str(db_event_name) + ""
    return event_url








async def count_all_Event():
    data = session.query(Event).count()
    return data










async def add_only_flyer(event_id: int, flyer: UploadFile = File(None), program_outline: UploadFile = File(None)):
    eventID = event_id

    flyer_name:str = flyer.filename
    program_outline_name:str = program_outline.filename
    is_eventID_update = session.query(Event).filter(Event.id == eventID).update({
            Event.flyer: flyer_name, Event.program_outline: program_outline_name
        }, synchronize_session=False)
    session.flush()
    session.commit()
    if not is_eventID_update:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Event with the id (" + str(event_id) + ") is not available")
    

    #save flyer
    with open(f'{IMAGEDIR}{flyer.filename}', "wb") as image:
        shutil.copyfileobj(flyer.file, image)


        #save program_outline
    with open(f'{PROGRAMOUTLINEDIR}{program_outline.filename}', "wb") as image:
        shutil.copyfileobj(program_outline.file, image)
    data = session.query(Event).filter(Event.id == event_id).one()
    return data












# from fastapi.responses import FileResponse

# @events_router.get("/read_image")
# async def read_image():
#     return FileResponse("app/flyers/kaleidoscope.jpg")

# async def add_event(event_name:str = Form(...), venue:str = Form(...),
#                 start_date:str = Form(...), end_date:str = Form(...),
#                 registration_time:str = Form(None) ,how_to_join:str = Form(None),
#                   number_of_participants:str = Form(None),
#                 description:str = Form(None), flyer: UploadFile = File(None),
#                 program_outline: UploadFile = File(None),
#                 current_admin: Admin = Depends(authentication.get_current_user)):
    
#     admin_id = current_admin.id

#     db_query = session.query(Event).filter(
#             Event.event_name == event_name
#         ).first()

#     if db_query is not None:
#         raise HTTPException(status_code=status.HTTP_303_SEE_OTHER,
#            detail=f"Event (" + \
#         str(event_name) + ") already exists")

#     flyer_name:str = flyer.filename

#     program_outline_name:str = program_outline.filename

#     new_event = Event()
#     new_event.event_name = event_name
#     new_event.venue = venue
#     new_event.flyer = flyer_name
#     new_event.program_outline = program_outline_name
#     new_event.start_date = start_date
#     new_event.end_date = end_date
#     new_event.how_to_join = how_to_join
#     new_event.registration_time = registration_time
#     new_event.number_of_participants = number_of_participants
#     new_event.description = description
#     new_event.admin_id = admin_id
#     new_event.status = "Active"
    
#     session.add(new_event)
#     session.flush()
#     session.refresh(new_event, attribute_names=['id'])
#     data = {
#         "event_name": new_event.event_name,
#         "venue": new_event.venue,
#         "status": new_event.status,
#         "flyer": new_event.flyer,
#         "start_date": new_event.start_date,
#         "end_date": new_event.end_date,
#         "admin_id": new_event.admin_id,
#         "registration_time": new_event.registration_time,
#         "number_of_participants": new_event.number_of_participants,
#         "description": new_event.description
#     }
#     session.commit()
#     session.close()

#     #save flyer
#     with open(f'{IMAGEDIR}{flyer.filename}', "wb") as image:
#         shutil.copyfileobj(flyer.file, image)

#     # Save program outline file
#     with open(f'{PROGRAMOUTLINEDIR}{program_outline.filename}', "wb") as image:
#         shutil.copyfileobj(program_outline.file, image)
#     return data