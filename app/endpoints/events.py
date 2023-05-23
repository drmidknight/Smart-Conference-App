from fastapi import FastAPI, APIRouter, status, Depends, Security, File, UploadFile, Form
from typing_extensions import Annotated
from app.schemas.schemas import *
from app.response.response import Response
from app.models.models import *
from app.utils.database import Database
from app.auth import authentication
from app.utils.config import *
from app.endpoints import admin
from fastapi.exceptions import HTTPException
from sqlalchemy import and_, desc, or_
from passlib.context import CryptContext
from fastapi_jwt_auth import AuthJWT
from fastapi.encoders import jsonable_encoder
from fastapi.security import (OAuth2PasswordBearer, OAuth2PasswordRequestForm)
from app.mail.sendmail import *
import uuid
from sqlalchemy.orm import load_only
from datetime import datetime, timedelta
import shutil



# APIRouter creates path operations for staffs module
router = APIRouter(
    prefix="/event",
    tags=["Event"],
    responses={404: {"description": "Not found"}},
)


IMAGEDIR = "app/endpoints/images/"

database = Database()
engine = database.get_db_connection()
session = database.get_db_session(engine)


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")









@router.post("/add", response_description="Event data added into the database")
async def add_event(event_name:str = Form(...), venue:str = Form(...),
                start_date:str = Form(...), end_date:str = Form(...),
                registration_time:str = Form(None) , number_of_participants:str = Form(None),
                description:str = Form(None), file: UploadFile = File(None),
                current_admin: Admin = Depends(authentication.get_current_user)):
    
    admin_id = current_admin.id

    response_code = 200
    db_query = session.query(Event).filter(or_(
            Event.event_name == event_name
        )).first()

    if db_query is not None:
        response_msg = "Event (" + \
        str(event_name) + ") already exists"
        error = True
        data = None
        return Response("ok", response_msg, data, response_code, error)

    flyer_name:str = file.filename

    new_event = Event()
    new_event.event_name = event_name
    new_event.venue = venue
    new_event.flyer = flyer_name
    new_event.start_date = start_date
    new_event.end_date = end_date
    new_event.registration_time = registration_time
    new_event.number_of_participants = number_of_participants
    new_event.description = description
    new_event.admin_id = admin_id
    new_event.status = "Active"
    
    session.add(new_event)
    session.flush()
    session.refresh(new_event, attribute_names=['id'])
    response_msg = "Event (" + \
        str(new_event.event_name) + ") created successfully"
    data = {"event_name": new_event.event_name}
    session.commit()
    session.close()

        #save flyer
    with open(f'{IMAGEDIR}{file.filename}', "wb") as image:
        shutil.copyfileobj(file.file, image)
    return Response("ok", response_msg, data, response_code, False)









@router.get("/getAllEvents")
async def all_event():
    data = session.query(Event).filter(Event.status == "Active").all()
    return Response("ok", "success", data, 200, False)









@router.get("/getEventById/{id}")
async def getEventById(id: str):
    try:
        db_data = session.query(Event).filter(Event.id == id).update({
            Event.status: "Active"
            }, synchronize_session=False)
        session.flush()
        session.commit()
        response_msg = "Event retrieved successfully"
        response_code = 200
        error = False 
        data = {"id": id}
        if db_data == 1:
            data = session.query(Event).filter(Event.id == id).one()
        elif db_data == 0:
            response_msg = "Event with id (" + \
        str(id) + ") does not exists"
            error = True
            data = None
            response_code = status.HTTP_404_NOT_FOUND
        return Response("ok", response_msg, data, response_code, error)
    except Exception as ex:
        print("Error : ", ex)






@router.put("/update")
async def updateAdmin(updateEvent: UpdateEventRequest):
    eventID = updateEvent.id
    try:
        is_eventID_update = session.query(Event).filter(Event.id == eventID).update({
            Event.event_name: updateEvent.event_name,
            Event.venue: updateEvent.venue,
            Event.start_date: updateEvent.start_date,
            Event.end_date: updateEvent.end_date,
            Event.registration_time: updateEvent.registration_time,
            Event.number_of_participants: updateEvent.number_of_participants,
            Event.description: updateEvent.description
        }, synchronize_session=False)
        session.flush()
        session.commit()
        response_msg = "Event updated successfully"
        response_code = 200
        error = False
        if is_eventID_update == 1:
            data = session.query(Event).filter(
                Event.id == eventID).one()

        elif is_eventID_update == 0:
            response_msg = "Event not updated. No Event found with this id :" + \
                str(eventID)
            error = True
            data = None
        return Response("ok", response_msg, data, response_code, error)
    except Exception as ex:
        print("Error : ", ex)












@router.get("/getEventByName/{event_name}")
async def getEventByName(event_name: str):
    try:
        db_data = session.query(Event).filter(Event.event_name == event_name).update({
            Event.status: "Active"
            }, synchronize_session=False)
        session.flush()
        session.commit()
        response_msg = "Event retrieved successfully"
        response_code = 200
        error = False 
        data = {"event_name": event_name}
        if db_data == 1:
            data = session.query(Event).filter(Event.event_name == event_name).one()
        elif db_data == 0:
            response_msg = "Event (" + \
        str(event_name) + ") does not exists"
            error = True
            data = None
            response_code = status.HTTP_404_NOT_FOUND
        return Response("ok", response_msg, data, response_code, error)
    except Exception as ex:
        print("Error : ", ex)











@router.delete("/delete/{id}")
async def deleteEvent(id: int):
    try:
        db_data = session.query(Event).filter(Event.id == id).update({
            Event.status: "InActive"
            }, synchronize_session=False)
        session.flush()
        session.commit()
        response_msg = "Event deleted successfully"
        response_code = 200
        error = False 
        data = {"id": id}
        if db_data == 1:
            data = session.query(Event).filter(Event.id == id).one()
        elif db_data == 0:
            response_msg = "Event not deleted. Event with id (" + \
        str(id) + ") not found"
            error = True
            data = None
            response_code = status.HTTP_404_NOT_FOUND
        return Response("ok", response_msg, data, response_code, error)
    except Exception as ex:
        print("Error : ", ex)






@router.get("/event_url/{event_name}")
async def generate_url(event_name: str):
    try:
        db_data = session.query(Event).filter(Event.event_name == event_name).update({
            Event.status: "Active"
            }, synchronize_session=False)
        session.flush()
        session.commit()
        response_msg = "Event retrieved successfully"
        response_code = 200
        error = False 
        data = {"event_name": event_name}
        if db_data == 1:
            data = session.query(Event).filter(Event.event_name == event_name).one()
        elif db_data == 0:
            response_msg = "Event (" + \
        str(event_name) + ") does not exists"
            error = True
            data = None
            response_code = status.HTTP_404_NOT_FOUND
        return Response("ok", response_msg, data, response_code, error)
    except Exception as ex:
        print("Error : ", ex)





@router.get("/countEvent")
async def count_all_Event():
    data = session.query(Event).count()
    return Response("ok", "Event retrieved successfully.", data, 200, False)
