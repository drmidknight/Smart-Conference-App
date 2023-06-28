from fastapi import APIRouter, status, Depends, File, UploadFile, Form
from routers.events.schemas.events import EventRequest, UpdateEventRequest
# from routers.admin.models.models import Admin
# from routers.events.models.models import Event
from models.models import Admin, Event
from utils.database import Database
from utils.config import settings
from auth import authentication
from fastapi.exceptions import HTTPException
from passlib.context import CryptContext
import shutil
from response.response import Response
from typing import Optional, List
from fastapi.responses import FileResponse
import os

 


IMAGEDIR = "app/routers/events/repo/"


PROGRAMOUTLINEDIR = "app/program_outlines/"




database = Database()
engine = database.get_db_connection()
session = database.get_db_session(engine)


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")







async def add_event(addEvent: EventRequest,
                    #flyer: Optional[UploadFile] = File(None),program_outline: Optional[UploadFile] = File(None),
                #current_admin: Admin = Depends(authentication.get_current_user)
                ):
    
    #admin_id = current_admin.id

    db_query = session.query(Event).filter(
            Event.event_name == addEvent.event_name
        ).first()

    if db_query is not None:
        raise HTTPException(status_code=status.HTTP_303_SEE_OTHER,
           detail=f"Event (" + \
        str(addEvent.event_name) + ") already exists")

    flyer_name = f"flyer-" + str(addEvent.event_name) + ".jpg"
    program_outline_name = f"program_outline-" + str(addEvent.event_name) + ".jpg"

    new_event = Event()
    new_event.event_name = addEvent.event_name
    new_event.venue = addEvent.venue
    new_event.start_date = addEvent.start_date
    new_event.end_date = addEvent.end_date
    new_event.how_to_join = addEvent.how_to_join
    new_event.registration_time = addEvent.registration_time
    new_event.number_of_participants = addEvent.number_of_participants
    new_event.description = addEvent.description
    new_event.flyer = flyer_name
    new_event.program_outline = program_outline_name
    #new_event.admin_id = admin_id
    new_event.status = "Active"
    
    session.add(new_event)
    session.flush()
    session.refresh(new_event, attribute_names=['id'])
    data = {
        "event_name": new_event.event_name,
        "venue": new_event.venue,
        "status": new_event.status,
        "program_outline": new_event.program_outline,
        "start_date": new_event.start_date,
        "end_date": new_event.end_date,
        "admin_id": new_event.admin_id,
        "registration_time": new_event.registration_time,
        "number_of_participants": new_event.number_of_participants,
        "description": new_event.description
    }
    session.commit()
    session.close()

    # try:
    #     flyer_contents = flyer.file.read()
    #     with open(flyer_name, 'wb') as f:
    #         f.write(flyer_contents)
    # except Exception:
    #     return {"message": "There was an error uploading flyer"}
    # finally:
    #     flyer_name


    # try:
    #     program_outline_contents = program_outline.file.read()
    #     with open(program_outline_name, 'wb') as f:
    #         f.write(program_outline_contents)
    # except Exception:
    #     return {"message": "There was an error uploading program_outline"}
    # finally:
    #     program_outline_name


    return data









async def all_event():
    data = session.query(Event).filter(Event.status == "Active").all()
    return data




#FileResponse("AG.jpg")


async def getEventById(id: str):
    data = session.query(Event).filter(Event.id == id).first()

    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Event with the id {id} is not available")

    #fileResponse = FileResponse(f'{data.flyer}')

    # db_data = {
    #     "flyer_name": data.event_name,
    # }

    return data











async def update_Event(updateEvent: UpdateEventRequest):
    eventID = updateEvent.id
    is_eventID_update = session.query(Event).filter(Event.id == eventID).update({
            Event.event_name: updateEvent.event_name,
            Event.venue: updateEvent.venue,
            Event.how_to_join: updateEvent.how_to_join,
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
    # event_url = f"flyer-" + str(db_event_name) + ".jpg"

    return event_url








async def count_all_Event():
    data = session.query(Event).count()
    return data











async def add_only_flyer(event_id: int, flyer: Optional[UploadFile] = File(None), program_outline: Optional[UploadFile] = File(None)):
    eventID = event_id
    
    db_data = session.query(Event).filter(Event.id == event_id).first()

    if not db_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Event with the id (" + str(event_id) + ") is not available")


    flyer_name = f"flyer-" + str(db_data.event_name) + ".jpg"
    program_outline_name = f"program_outline-" + str(db_data.event_name) + ".pdf"

    is_eventID_update = session.query(Event).filter(Event.id == eventID).update({
            Event.flyer: flyer_name, Event.program_outline: program_outline_name
        }, synchronize_session=False)
    session.flush()
    session.commit()
  

       # get flyer destination path
    flyer_dest = os.path.join(settings.flyer_upload_dir, flyer_name)
    print(flyer_dest)


       # get program_outline destination path
    program_outline_dest = os.path.join(settings.program_outline_upload_dir, program_outline_name)
    print(program_outline_dest)



    try:
        flyer_contents = flyer.file.read()
        with open(flyer_dest, 'wb') as f:
            f.write(flyer_contents)
    except Exception:
        return {"message": "There was an error uploading flyer"}
    finally:
        flyer_name


    try:
        program_outline_contents = program_outline.file.read()
        with open(program_outline_dest, 'wb') as f:
            f.write(program_outline_contents)
    except Exception:
        return {"message": "There was an error uploading program_outline"}
    finally:
        program_outline_name


    # #save flyer
    # with open(f'{flyer.filename}', "wb") as image:
    #     shutil.copyfileobj(flyer.file, image)


    #     #save program_outline
    # with open(f'{program_outline.filename}', "wb") as image:
    #     shutil.copyfileobj(program_outline.file, image)



    #data = session.query(Event).filter(Event.id == event_id).one()
    return is_eventID_update
    if not db_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Event with the id (" + str(event_id) + ") is not available")


    flyer_name = f"flyer-" + str(db_data.event_name) + ".jpg"
    program_outline_name = f"program_outline-" + str(db_data.event_name) + ".pdf"

    is_eventID_update = session.query(Event).filter(Event.id == eventID).update({
            Event.flyer: flyer_name, Event.program_outline: program_outline_name
        }, synchronize_session=False)
    session.flush()
    session.commit()
  

       # get flyer destination path
    flyer_dest = os.path.join(settings.flyer_upload_dir, flyer_name)
    print(flyer_dest)


       # get program_outline destination path
    program_outline_dest = os.path.join(settings.program_outline_upload_dir, program_outline_name)
    print(program_outline_dest)



    try:
        flyer_contents = flyer.file.read()
        with open(flyer_dest, 'wb') as f:
            f.write(flyer_contents)
    except Exception:
        return {"message": "There was an error uploading flyer"}
    finally:
        flyer_name


    try:
        program_outline_contents = program_outline.file.read()
        with open(program_outline_dest, 'wb') as f:
            f.write(program_outline_contents)
    except Exception:
        return {"message": "There was an error uploading program_outline"}
    finally:
        program_outline_name


    # #save flyer
    # with open(f'{flyer.filename}', "wb") as image:
    #     shutil.copyfileobj(flyer.file, image)


    #     #save program_outline
    # with open(f'{program_outline.filename}', "wb") as image:
    #     shutil.copyfileobj(program_outline.file, image)



    #data = session.query(Event).filter(Event.id == event_id).one()
    return is_eventID_update












# from fastapi.responses import FileResponse

# @events_router.get("/read_image")
# async def read_image():
#     return FileResponse("app/flyers/kaleidoscope.jpg")


async def add_event_with_files(event_name:str = Form(...), venue:str = Form(...),
                start_date:str = Form(...), end_date:str = Form(...),
                registration_time:str = Form(None) ,how_to_join:str = Form(None),
                  number_of_participants:str = Form(None),
                description:str = Form(None), flyer: Optional[UploadFile] = File(None),
                program_outline: Optional[UploadFile] = File(None),
                #current_admin: Admin = Depends(authentication.get_current_user)
                ):

    #admin_id = current_admin.id

    db_query = session.query(Event).filter(
            Event.event_name == event_name
        ).first()

    if db_query is not None:
        raise HTTPException(status_code=status.HTTP_303_SEE_OTHER,
           detail=f"Event (" + \
        str(event_name) + ") already exists")



    flyer_name = f"flyer-" + str(event_name) + ".jpg"
    program_outline_name = f"program_outline-" + str(event_name) + ".pdf"

    new_event = Event()
    new_event.event_name = event_name
    new_event.venue = venue
    new_event.flyer = flyer_name
    new_event.program_outline = program_outline_name
    new_event.start_date = start_date
    new_event.end_date = end_date
    new_event.how_to_join = how_to_join
    new_event.registration_time = registration_time
    new_event.number_of_participants = number_of_participants
    new_event.description = description
    #new_event.admin_id = admin_id
    new_event.status = "Active"
    
    session.add(new_event)
    session.flush()
    session.refresh(new_event, attribute_names=['id'])
    data = {
        "event_name": new_event.event_name,
        "venue": new_event.venue,
        "status": new_event.status,
        "flyer_name": new_event.flyer,
        "program_outline_name": new_event.program_outline,
        "start_date": new_event.start_date,
        "end_date": new_event.end_date,
        #"admin_id": new_event.admin_id,
        "registration_time": new_event.registration_time,
        "number_of_participants": new_event.number_of_participants,
        "description": new_event.description
    }
    session.commit()
    session.close()




   # get flyer destination path
    flyer_dest = os.path.join(settings.flyer_upload_dir, flyer_name)
    print(flyer_dest)


       # get program_outline destination path
    program_outline_dest = os.path.join(settings.program_outline_upload_dir, program_outline_name)
    print(program_outline_dest)



    try:
        flyer_contents = flyer.file.read()
        with open(flyer_dest, 'wb') as f:
            f.write(flyer_contents)
    except Exception:
        return {"message": "There was an error uploading flyer"}
    finally:
        flyer_name


    try:
        program_outline_contents = program_outline.file.read()
        with open(program_outline_dest, 'wb') as f:
            f.write(program_outline_contents)
    except Exception:
        return {"message": "There was an error uploading program_outline"}
    finally:
        program_outline_name



    #     #save flyer
    # with open(f'{flyer_name}', "wb") as image:
    #     shutil.copyfileobj(flyer.file, image)

    # # Save program outline file
    # with open(f'{program_outline_name}', "wb") as image:
    #     shutil.copyfileobj(program_outline.file, image)
    return data


















