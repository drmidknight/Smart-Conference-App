from fastapi.security import OAuth2PasswordRequestForm
from fastapi import status, Depends
from mail.sendmail import sendemailtonewusers,send_reset_password
from fastapi.exceptions import HTTPException
from passlib.context import CryptContext
from routers.admin.schemas import admin
from utils.database import Database
from utils.config import settings
from models.models import Admin
from auth import authentication
from datetime import timedelta





database = Database()
engine = database.get_db_connection()
session = database.get_db_session(engine)


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")





## function to authentication all admin and users
async def admin_authentication(form_data: OAuth2PasswordRequestForm = Depends()):
    
    data=session.query(Admin).filter(Admin.email==form_data.username).first()

    if data and pwd_context.verify(form_data.password, data.password):
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = authentication.create_access_token(data={"email": data.email}, expires_delta=access_token_expires)

        db_data = {
            "access_token":access_token,
            "token_type": "bearer"
        }

        return db_data


    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                        detail="Invalid login credential"                   
    )










## function to create new admin and users

async def create_admin(adminRequest: admin.AdminRequest):

    db_query = session.query(Admin).filter(Admin.email == adminRequest.email).first()
 
    if db_query:
        raise HTTPException(status_code=status.HTTP_303_SEE_OTHER,
           detail="Admin or User with email (" + \
        str(adminRequest.email) + ") already exists")
    
    new_admin = Admin(**adminRequest.dict())
    new_admin.reset_password_token = authentication.generate_reset_password_token()
    new_admin.password = None
    session.add(new_admin)
    session.flush()
    session.refresh(new_admin, attribute_names=['id'])
    await sendemailtonewusers([adminRequest.email], new_admin)
    session.commit()
    session.close()
    return new_admin










## function to get all admin and users base on their active status

async def get_all():
    data = session.query(Admin).all()
    return data






## function to get admin or users base on id

async def getAdminById(id: str):
    data = session.query(Admin).filter(Admin.id == id).all()
    
    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Admin or User with the id {id} is not found")
    return data






## function to update admin or users base on id

async def updateAdmin(updateAdmin: admin.UpdateAdmin):
    adminID = updateAdmin.id
    is_adminID_update = session.query(Admin).filter(Admin.id == adminID).update({
            Admin.name: updateAdmin.name,
            Admin.contact: updateAdmin.contact,
            Admin.email: updateAdmin.email,
            Admin.usertype: updateAdmin.usertype,
            Admin.event_id: updateAdmin.event_id
        }, synchronize_session=False)
    session.flush()
    session.commit()
    if not is_adminID_update:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail="Admin or User with the id (" + str(adminID) + ") not found")

    data = session.query(Admin).filter(Admin.id == adminID).one()
    return data











## function to get admin or user base on email
async def get_by_email(email: str):

    user_db_data = session.query(Admin).filter(Admin.email == email).update({
        Admin.password : None,
        Admin.reset_password_token : authentication.generate_reset_password_token()
    }, synchronize_session=False)
    session.flush()
    session.commit()
    
    if not user_db_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail="Admin or User with the email (" + str(email) + ") is not found")
    
    data = session.query(Admin).filter(Admin.email == email).one()
    await send_reset_password([email], data)
    return data









## function to get admin or user base on token
async def get_by_token(token: str):

    user_db_data = session.query(Admin).filter(Admin.reset_password_token == token).update({
        Admin.password : None
    }, synchronize_session=False)
    session.flush()
    session.commit()
    
    if not user_db_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid Token")

    data = session.query(Admin).filter(Admin.reset_password_token == token).one()
    return data









## function to delete all admin and users base on id
async def deleteAdmin(id: str):
    db_data = session.query(Admin).filter(Admin.id == id).update({
            Admin.status: "InActive"
            }, synchronize_session=False)
    session.flush()
    session.commit()
    if not db_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Admin or User with the id {id} is not found")

    data = session.query(Admin).filter(Admin.id == id).one()
    return data

    





## function to count all admin and users
async def count_all_Admin():
    data = session.query(Admin).count()
    return data














async def update_user_after_reset_password(update: admin.UpdateAdmin):
    staffID = update.id
    is_staffID_update = session.query(Admin).filter(Admin.id == staffID).update({
        Admin.reset_password_token : None,
        Admin.hashed_password : pwd_context.hash(update.password)
        }, synchronize_session=False)
    session.flush()
    session.commit()
    if not is_staffID_update:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail="Staff with the id (" + str(staffID) + ") is not found")

    data = session.query(Admin).filter(Admin.id == staffID).one()
    return data