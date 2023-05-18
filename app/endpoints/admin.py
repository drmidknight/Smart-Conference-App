from fastapi import APIRouter, status, Depends
from app.schemas.schemas import *
from app.response.response import Response
from app.models.models import *
from app.utils.database import Database
from fastapi.exceptions import HTTPException
from sqlalchemy import and_, desc, or_
from passlib.context import CryptContext
from fastapi_jwt_auth import AuthJWT
from fastapi.encoders import jsonable_encoder
from fastapi.security import (OAuth2PasswordBearer, OAuth2PasswordRequestForm)
from app.auth.authentication import *
from app.mail.sendmail import *
from uuid import uuid4
from sqlalchemy.orm import load_only
from typing import Union, Any
from app.utils.config import *


# APIRouter creates path operations for staffs module
router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
    responses={404: {"description": "Not found"}},
)


oath2_scheme = OAuth2PasswordBearer(tokenUrl = 'token')


database = Database()
engine = database.get_db_connection()
session = database.get_db_session(engine)


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")




@router.post('/login')
async def admin_login(email:str, password:str):
    data=session.query(Admin).filter(Admin.email==email).first()

    if data and pwd_context.verify(password, data.password):
        access_token = create_access_token(data={"email": data.email, "contact": data.contact})

        return{
            "access":access_token,
            "token_type": "bearer"
            }

    return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                        detail="Invalid login credential"                   
    )







@router.post("/add", response_description="Admin data added into the database")
async def add_admin(adminRequest: AdminRequest):

    response_code = 200
    db_query = session.query(Admin).filter(or_(
            Admin.email == adminRequest.email,
            Admin.contact == adminRequest.contact
        )).first()

    if db_query is not None:
        response_msg = "Admin with email or phone number (" + \
        str(adminRequest.email) + ") already exists"
        error = True
        data = None
        return Response("ok", response_msg, data, response_code, error)

    new_admin = Admin()
    new_admin.admin_name = adminRequest.admin_name
    new_admin.email = adminRequest.email
    new_admin.contact = adminRequest.contact
    new_admin.reset_password_token = create_access_token(new_admin)
    new_admin.status = "Active"
    
    session.add(new_admin)
    session.flush()
    # get id of the inserted staff
    session.refresh(new_admin, attribute_names=['id'])
    await sendEmailToNewAdmin([adminRequest.email], new_admin)
    # data = {"staff_id": new_admin.id}
    data = {"Token": new_admin.reset_password_token}
    session.commit()
    session.close()
    return Response("ok", "Admin added successfully", data, response_code, False)




@router.get("/getAllStaffs")
async def all_staff():
    data = session.query(Admin).all()
    return Response("ok", "success", data, 200, False)







@router.get("/findStaffById")
async def findStaffById(id: str):
    response_message = "Staff retrieved successfully"
    data = None
    try:
        data = session.query(Admin).filter(Admin.id == id).one()
    except Exception as ex:
        print("Error", ex)
        response_message = "Staff Not found"
    error = False
    return Response("ok", "success", data, 200, False)








@router.put("/updateCourse")
async def update_course(update_course: UpdateCourseRequest):
    course_id = update_course.id
    try:
        is_course_update = session.query(Admin).filter(Admin.id == course_id).update({
            Admin.course_name: update_course.course_name
        }, synchronize_session=False)
        session.flush()
        session.commit()
        response_msg = "Course updated successfully"
        response_code = 200
        error = False
        if is_course_update == 1:
            # After successful update, retrieve updated data from db
            data = session.query(Admin).filter(
                Admin.id == course_id).one()

        elif is_course_update == 0:
            response_msg = "Course not updated. No course found with this id :" + \
                str(course_id)
            error = True
            data = None
        return Response(data, response_code, response_msg, error)
    except Exception as ex:
        print("Error : ", ex)










@router.delete("/deleteCourseById/{id}")
async def delete_course(id: str):
    try:
        is_course_updated = session.query(Admin).filter(Admin.id == id).update({
            Admin.status: "Inactive"}, synchronize_session=False)
        session.flush()
        session.commit()
        response_msg = "Course deleted successfully"
        response_code = 200
        error = False
        data = {"id": id}
        if is_course_updated == 0:
            response_msg = "Course not deleted. No Course found with this id :" + \
                str(id)
            error = True
            data = None
        return Response(data, response_code, response_msg, error)
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
    




























@router.put("/updateStaffDetailsAfterResetPassword")
async def updateStaffDetailsAfterResetPassword(updateStaffRequest: UpdateStaffRequest):
    staffDetailID = updateStaffRequest.id
    try:
        is_staffDetailID_update = session.query(Admin).filter(Admin.id == staffDetailID).update({
            Admin.reset_password_token: None,
            Admin.password: pwd_context.hash(updateStaffRequest.password)
        }, synchronize_session=False)
        session.flush()
        session.commit()
        response_msg = "Staff Detail updated successfully"
        response_code = 200
        error = False
        if is_staffDetailID_update == 1:
            # After successful update, retrieve updated data from db
            data = session.query(Admin).filter(
                Admin.id == staffDetailID).one()

        elif is_staffDetailID_update == 0:
            response_msg = "Staff Detail not updated. No staff Detail found with this id :" + \
                str(staffDetailID)
            error = True
            data = None
        return Response("ok", response_msg, data, response_code, error)
    except Exception as ex:
        print("Error : ", ex)











@router.post('/login')
async def staff_login(email:str, password:str, Authorize:AuthJWT=Depends()):
    data=session.query(Admin).filter(Admin.email==email).first()

    if data and pwd_context.verify(password, data.password):
        access_token = Authorize.create_access_token(subject=data.name)
        refresh_token = Authorize.create_refresh_token(subject=data.name)

        response={
            "access":access_token,
            "refresh":refresh_token
        }

        response_code = status.HTTP_200_OK
        return Response("ok", "success", data, response_code, False)

    return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                        detail="Invalid login credential"                   
    )