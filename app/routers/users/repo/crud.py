from fastapi import APIRouter, status, Depends
from routers.users.schemas import users
from models.models import Users
from utils.database import Database
from auth import authentication
from fastapi.exceptions import HTTPException
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm
from mail.sendmail import (sendEmailToNewUsers, generate_reset_password_token)
from utils.config import settings
from datetime import timedelta





database = Database()
engine = database.get_db_connection()
session = database.get_db_session(engine)


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")






async def Users_authentication(form_data: OAuth2PasswordRequestForm = Depends()):
    
    data=session.query(users).filter(users.email==form_data.username).first()

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












async def create_user(userRequest: users.UserRequest):

    db_query = session.query(Users).filter(Users.email == userRequest.email).first()
 
    if db_query is not None:
        raise HTTPException(status_code=status.HTTP_303_SEE_OTHER,
           detail="User with email (" + \
        str(userRequest.email) + ") already exists")
    
    new_Users = Users()
    new_Users.name = userRequest.name
    new_Users.email = userRequest.email
    new_Users.reset_password_token = generate_reset_password_token()
    new_Users.status = "Active"
    session.add(new_Users)
    session.flush()
    session.refresh(new_Users, attribute_names=['id'])
    #await sendEmailToNewUsers([userRequest.email], new_Users)
    session.commit()
    session.close()
    return new_Users













async def get_all_Users():
    data = session.query(Users).filter(Users.status == "Active").all()
    return data




async def get_User_By_Id(id: str):
    data = session.query(Users).filter(Users.id == id).all()
    
    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with the id {id} is not found")
    return data








async def update_User(updateUsers: users.UpdateUser):
    UsersID = updateUsers.id
    is_UsersID_update = session.query(Users).filter(Users.id == UsersID).update({
            Users.name: updateUsers.name,
            Users.email: updateUsers.email
        }, synchronize_session=False)
    session.flush()
    session.commit()
    if not is_UsersID_update:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail="User with the id (" + str(UsersID) + ") is not found")

    data = session.query(Users).filter(Users.id == UsersID).one()
    return data










async def get_User_By_Email(email: str):
    data = session.query(Users).filter(Users.email == email).all()
    
    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User with the email {email} is not found")
    return data



















async def delete_User(id: str):
    db_data = session.query(Users).filter(Users.id == id).update({
            Users.status: "InActive"
            }, synchronize_session=False)
    session.flush()
    session.commit()
    if not db_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail="User with the id {id} is not found")

    data = session.query(Users).filter(Users.id == id).one()
    return data

    






async def count_all_Users():
    data = session.query(Users).count()
    return data
