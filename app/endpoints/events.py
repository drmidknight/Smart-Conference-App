from fastapi import FastAPI, APIRouter, status, Depends, Security, File, UploadFile
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
async def add_Event(eventRequest: EventRequest,
                    #file: UploadFile = File(...)
                    #current_user: Admin = Depends(authentication.get_current_user)
                    ):
    
    #user_id=current_user.id
    response_code = 200
    db_query = session.query(Event).filter(or_(
            Event.event_name == eventRequest.event_name
        )).first()

    if db_query is not None:
        response_msg = "Event (" + \
        str(eventRequest.event_name) + ") already exists"
        error = True
        data = None
        return Response("ok", response_msg, data, response_code, error)

    #flyer_name:str = file.filename

    new_event = Event()
    new_event.event_name = eventRequest.event_name
    new_event.venue = eventRequest.venue
    #new_event.flyer = flyer_name
    new_event.start_date = eventRequest.start_date
    new_event.end_date = eventRequest.end_date
    new_event.registration_time = eventRequest.registration_time
    new_event.number_of_participants = eventRequest.number_of_participants
    new_event.description = eventRequest.description
    #new_event.admin_id = admin_id.id
    new_event.status = "Active"
    
    session.add(new_event)
    session.flush()
    session.refresh(new_event, attribute_names=['id'])
    data = {"event_name": new_event.event_name}
    session.commit()
    session.close()
    return Response("ok", "Event added successfully", data, response_code, False)




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
        response_msg = "Admin retrieved successfully"
        response_code = 200
        error = False 
        data = {"id": id}
        if db_data == 1:
            data = session.query(Admin).filter(Admin.id == id).one()
        elif db_data == 0:
            response_msg = "Admin with id (" + \
        str(id) + ") does not exists"
            error = True
            data = None
            response_code = status.HTTP_404_NOT_FOUND
        return Response("ok", response_msg, data, response_code, error)
    except Exception as ex:
        print("Error : ", ex)






@router.put("/update")
async def updateAdmin(updateAdmin: UpdateAdmin):
    adminID = updateAdmin.id
    try:
        is_adminID_update = session.query(Admin).filter(Admin.id == adminID).update({
            Admin.admin_name: updateAdmin.admin_name,
            Admin.contact: updateAdmin.contact,
            Admin.email: updateAdmin.email
        }, synchronize_session=False)
        session.flush()
        session.commit()
        response_msg = "Admin updated successfully"
        response_code = 200
        error = False
        if is_adminID_update == 1:
            # After successful update, retrieve updated data from db
            data = session.query(Admin).filter(
                Admin.id == adminID).one()

        elif is_adminID_update == 0:
            response_msg = "Admin not updated. No Admin found with this id :" + \
                str(adminID)
            error = True
            data = None
        return Response("ok", response_msg, data, response_code, error)
    except Exception as ex:
        print("Error : ", ex)










@router.post("/getAdminByEmail/{email}")
async def getAdminByEmail(email: str):
    try:
        db_data = session.query(Admin).filter(Admin.email == email).update({
            Admin.status: "Active"
            }, synchronize_session=False)
        session.flush()
        session.commit()
        response_msg = "Admin retrieved successfully"
        response_code = 200
        error = False 
        data = {"email": email}
        if db_data == 1:
            data = session.query(Admin).filter(Admin.email == email).one()
        elif db_data == 0:
            response_msg = "Admin with email (" + \
        str(email) + ") does not exists"
            error = True
            data = None
            response_code = status.HTTP_404_NOT_FOUND
        return Response("ok", response_msg, data, response_code, error)
    except Exception as ex:
        print("Error : ", ex)


















@router.delete("/delete/{id}")
async def deleteEvent(id: str):
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








@router.get("/countStaff")
async def count_all_staff():
    data = session.query(Admin).count()
    return Response("ok", "Staff retrieved successfully.", data, 200, False)






@router.get("/getInstructors")
async def getInstructors():
    data = None
    data = session.query(Admin).filter(or_(
        Admin.usertype == "Course Cordinator",
        Admin.usertype == "Faculty", 
        Admin.usertype == "Instructor"
        )).all()
    return Response("ok", "success", data, 200, False)






# @router.get("/getStaffDetails")
# async def getStaffDetails(token: str):
#     data = session.query(Admin).filter(Admin.reset_password_token == token).all()

#     if data is not None:
#          response_message = "Staff retrieved successfully"
#          response_code = status.HTTP_200_OK
#          return Response("ok", response_message, data, response_code, False)
    
#     return HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#             detail="Staff not found"
#         )







@router.get("/getStaffDetails")
async def getStaffDetails(token: str):
    try:
        db_data = session.query(Admin).filter(Admin.reset_password_token == token).update({
            Admin.password: None
            }, synchronize_session=False)
        session.flush()
        session.commit()
        response_msg = "Staff retrieved successfully"
        response_code = 200
        error = False 
        data = {"token": token}
        if db_data == 1:
            data = session.query(Admin).filter(Admin.reset_password_token == token).one()
        elif db_data == 0:
            response_msg = "Invalid Token"
            error = True
            data = None
            response_code = status.HTTP_404_NOT_FOUND
        return Response("ok", response_msg, data, response_code, error)
    except Exception as ex:
        print("Error : ", ex)









@router.post("/sendResetPasswordLinkToStaffEmail")
async def sendResetPasswordLinkToStaffEmail(email: str):
    try:
        db_data = session.query(Admin).filter(Admin.email == email).update({
            Admin.password: None,
            Admin.reset_password_token: generate_reset_password_token()
            }, synchronize_session=False)
        session.flush()
        session.commit()
        response_msg = "Staff retrieved successfully"
        response_code = 200
        error = False 
        data = {"email": email}
        if db_data == 1:
            data = session.query(Admin).filter(Admin.email == email).one()
            await send_Reset_Password_LinkToStaffEmail([email], data)
        elif db_data == 0:
            response_msg = "No Staff found with this email :" + \
                str(email)
            error = True
            data = None
            response_code = status.HTTP_404_NOT_FOUND
        return Response("ok", response_msg, data, response_code, error)
    except Exception as ex:
        print("Error : ", ex)
    

import shutil
app = FastAPI()


# @app.post("/flyer")
# async def flyer(file: UploadFile = File(...)):

#     #file.filename = f"{flyerIncrement()}.jpg"
#     file_location = f"images/{file.filename}"
#     filename = file.filename
#     contents = await file.read()

#     #save flyer
#     with open(f"{IMAGEDIR}{filename}", "wb+") as f:
#         f.write(contents)

#     return {"filename": filename}




# @router.post("/flyer")
# async def flyer(file: UploadFile = File(...)):

#     file.filename = f"{flyerIncrement()}.jpg"
#     #file_location = f"images/{file.filename}"
#     # filename = file.filename
#     contents = await file.read()

#     #save flyer
#     with open(f"{file.filename}", "wb") as image:
#         image.write(contents)

#     return {"filename": file.filename}






# @router.post("/flyer")
# async def flyer(file: UploadFile = File(...)):

#     #file.filename = f"{flyerIncrement()}.jpg"
#     #file_location = f"images/{file.filename}"
#     # filename = file.filename
#     # contents = await file.read()

#     #save flyer
#     with open(f'{IMAGEDIR}{file.filename}', "wb") as image:
#         shutil.copyfileobj(file.file, image)

#     return {"filename": file.filename}


def flyerIncrement(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))