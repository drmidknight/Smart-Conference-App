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
from app.utils.config import settings


# APIRouter creates path operations for staffs module
router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
    responses={404: {"description": "Not found"}},
)




database = Database()
engine = database.get_db_connection()
session = database.get_db_session(engine)


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")



@router.post('/login', response_model=Token)
async def admin_login(form_data: OAuth2PasswordRequestForm = Depends()):
    
    data=session.query(Admin).filter(Admin.email==form_data.username).first()

    if data and pwd_context.verify(form_data.password, data.password):
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = authentication.create_access_token(data={"email": data.email}, expires_delta=access_token_expires)

        return{
            "access_token":access_token,
            "token_type": "bearer",
            "email": data.email
            }


    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                        detail="Invalid login credential"                   
    )







@router.post("/add", response_description="Admin data added into the database")
async def add_admin(adminRequest: AdminRequest):

    db_query = session.query(Admin).filter(Admin.email == adminRequest.email).filter(
        Admin.contact == adminRequest.contact).first()
 
    if db_query is not None:
        raise HTTPException(status_code=status.HTTP_303_SEE_OTHER,
           detail=f"Admin with email or phone number (" + \
        str(adminRequest.email) + ") already exists")
    
    new_admin = Admin()
    new_admin.admin_name = adminRequest.admin_name
    new_admin.email = adminRequest.email
    new_admin.contact = adminRequest.contact
    new_admin.reset_password_token = generate_reset_password_token()
    new_admin.status = "Active"
    session.add(new_admin)
    session.flush()
    session.refresh()
    #await sendEmailToNewAdmin([adminRequest.email], new_admin)
    session.commit()
    session.close()
    return new_admin






@router.get("/getAllAdmin")
async def all_admin():
    data = session.query(Admin).filter(Admin.status == "Active").all()
    return data




@router.get("/getAdminById/{id}")
async def getAdminById(id: str):
    data = session.query(Admin).filter(Admin.id == id).all()
    
    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Admin with the id {id} is not found")
    return data







@router.put("/update")
async def updateAdmin(updateAdmin: UpdateAdmin):
    adminID = updateAdmin.id
    is_adminID_update = session.query(Admin).filter(Admin.id == adminID).update({
            Admin.admin_name: updateAdmin.admin_name,
            Admin.contact: updateAdmin.contact,
            Admin.email: updateAdmin.email
        }, synchronize_session=False)
    session.flush()
    session.commit()
    if not is_adminID_update:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Admin with the id (" + str(adminID) + ") is not found")

    data = session.query(Admin).filter(Admin.id == adminID).one()
    return data










@router.get("/getAdminByEmail/{email}")
async def getAdminByEmail(email: str):
    data = session.query(Admin).filter(Admin.email == email).all()
    
    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Admin with the email {email} is not found")
    return data


















@router.delete("/delete/{id}")
async def deleteAdmin(id: str):
    db_data = session.query(Admin).filter(Admin.id == id).update({
            Admin.status: "InActive"
            }, synchronize_session=False)
    session.flush()
    session.commit()
    if not db_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Admin with the id {id} is not found")

    data = session.query(Admin).filter(Admin.id == id).one()
    return data

    








@router.get("/countAdmin")
async def count_all_Admin():
    data = session.query(Admin).count()
    return data
