from fastapi import APIRouter, status, Depends, Security
from app.schemas.schemas import *
from app.response.response import Response
from app.models.models import *
from app.utils.database import Database
from app.auth import authentication
from fastapi.exceptions import HTTPException
from sqlalchemy import and_, desc, or_
from passlib.context import CryptContext
from fastapi_jwt_auth import AuthJWT
from fastapi.encoders import jsonable_encoder
from fastapi.security import (OAuth2PasswordBearer, OAuth2PasswordRequestForm)
from app.mail.sendmail import *
from uuid import uuid4
from sqlalchemy.orm import load_only
from typing import Union, Any
from app.utils.config import *


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









@router.post("/add", response_description="Participant data added into the database")
async def add_admin(participantRequest: ParticipantRequest):
    response_code = 200
    db_query = session.query(Participant).filter(or_(
            Participant.email == participantRequest.email,
            Participant.phone_number == participantRequest.phone_number
        )).first()

    if db_query is not None:
        response_msg = "Participant with email or phone number (" + \
        str(participantRequest.email) + ") already exists"
        error = True
        data = None
        return Response("ok", response_msg, data, response_code, error)

    new_participant = Participant()
    new_participant.name = participantRequest.name
    new_participant.phone_number = participantRequest.phone_number
    new_participant.gender = participantRequest.gender
    new_participant.email = participantRequest.email
    new_participant.organization = participantRequest.organization
    new_participant.attend_by = participantRequest.attend_by
    new_participant.registration_time = participantRequest.registration_time
    new_participant.location = participantRequest.location
    new_participant.event_id = participantRequest.event_id
    new_participant.status = 0
    
    session.add(new_participant)
    session.flush()
    session.refresh(new_participant, attribute_names=['id'])
    #await sendEmailToNewParticipant([new_participant.email], new_participant)
    data = {
            "id": new_participant.id,
            "email": new_participant.email
            }
    session.commit()
    session.close()
    return Response("ok", "Participant added successfully", data, response_code, False)






@router.get("/getAllParticipant")
async def all_Participant():
    data = session.query(Participant).all()
    return Response("ok", "success", data, 200, False)





@router.get("/getParticipantById/{id}")
async def get_Participant_By_Id(id: int):
        
        db_data = session.query(Participant).filter(Participant.id == id).all()
        
        if db_data is not None:
            response_msg = "Participant retrieved successfully"
            response_code = 200
            error = False 
            return Response("ok", response_msg, db_data, response_code, error)


        response_msg = "No Participant found with this id :" + \
        int(id)
        error = True
        data = None
        response_code = 404
        return Response("ok", response_msg, data, response_code, error)
    








@router.put("/update")
async def updateParticipant(updateParticipant: UpdateParticipant):
    participant_id = updateParticipant.id
    try:
        is_Participant_update = session.query(Participant).filter(Participant.id == participant_id).update({
            Participant.name: updateParticipant.name,
            Participant.phone_number: updateParticipant.phone_number,
            Participant.gender: updateParticipant.gender,
            Participant.email: updateParticipant.email,
            Participant.organization: updateParticipant.organization,
            Participant.attend_by: updateParticipant.attend_by,
            Participant.registration_time: updateParticipant.registration_time,
            Participant.location: updateParticipant.location,
            Participant.event_id: updateParticipant.event_id,
            Participant.status: 1
        }, synchronize_session=False)
        session.flush()
        session.commit()
        response_msg = "Participant updated successfully"
        response_code = 200
        error = False
        if is_Participant_update == 1:
            # After successful update, retrieve updated data from db
            data = session.query(Participant).filter(
                Participant.id == participant_id).one()

        elif is_Participant_update == 0:
            response_msg = "Participant not updated. No Participant found with this id :" + \
                str(participant_id)
            error = True
            data = None
        return Response("ok", response_msg, data, response_code, error)
    except Exception as ex:
        print("Error : ", ex)












@router.get("/phone_number_email/{phone_number_email}")
async def phone_number_email(phone_number_email: str):
    try:
        response_msg = "Participant retrieved successfully"
        response_code = 200
        error = False 
        if "@" in phone_number_email:
            data = session.query(Participant).filter(Participant.email == phone_number_email).all()
        elif "@" not in phone_number_email:
            data = session.query(Participant).filter(Participant.phone_number == phone_number_email).all()
        else:
            response_msg = "Email or Phone Number (" + str(phone_number_email) + ") does not exists"
            error = True
            data = None
            response_code = status.HTTP_404_NOT_FOUND
        return Response("ok", response_msg, data, response_code, error)
    except Exception as ex:
        print("Error : ", ex)











@router.get("/participantByattend_by/{attend_by}")
async def get_Participant_By_attend_by(attend_by: str):
    try:
        response_msg = "Participant retrieved successfully"
        response_code = 200
        error = False 
        if attend_by == "virtual":
            data = session.query(Participant).filter(Participant.attend_by == attend_by).all()
        elif attend_by == "onsite":
            data = session.query(Participant).filter(Participant.attend_by == attend_by).all()
        else:
            response_msg = "Attend by (" + str(attend_by) + ") does not exists"
            error = True
            data = None
            response_code = status.HTTP_404_NOT_FOUND
        return Response("ok", response_msg, data, response_code, error)
    except Exception as ex:
        print("Error : ", ex)










@router.delete("/delete/{id}")
async def deleteParticipant(id: str):
    try:
        db_data = session.query(Participant).filter(Participant.id == id).update({
            Participant.status: 0
            }, synchronize_session=False)
        session.flush()
        session.commit()
        response_msg = "Participant deleted successfully"
        response_code = 200
        error = False 
        data = {"id": id}
        if db_data == 1:
            data = session.query(Participant).filter(Participant.id == id).one()
        elif db_data == 0:
            response_msg = "Participant not deleted. Participant with id (" + \
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
    




























# @router.post('/login')
# async def staff_login(email:str, password:str, Authorize:AuthJWT=Depends()):
#     data=session.query(Admin).filter(Admin.email==email).first()

#     if data and pwd_context.verify(password, data.password):
#         access_token = Authorize.create_access_token(subject=data.name)
#         refresh_token = Authorize.create_refresh_token(subject=data.name)

#         response={
#             "access":access_token,
#             "refresh":refresh_token
#         }

#         response_code = status.HTTP_200_OK
#         return Response("ok", "success", data, response_code, False)

#     return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
#                         detail="Invalid login credential"                   
#     )