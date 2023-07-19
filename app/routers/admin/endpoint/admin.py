from fastapi.security import OAuth2PasswordRequestForm
from passlib.context import CryptContext
from routers.admin.schemas import admin
from fastapi import APIRouter, Depends
from utils.database import Database
from routers.admin.repo import crud





# APIRouter creates path operations for admin and users module
admin_router = APIRouter(
    prefix="/admin",
    tags=["Admin and Users"],
    responses={404: {"description": "Not found"}},
)




database = Database()
engine = database.get_db_connection()
session = database.get_db_session(engine)


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")




## function to authentication all admin and users
@admin_router.post('/login', response_model=admin.Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    
    return await crud.admin_authentication(form_data)






## function to create new admin and users
@admin_router.post("/add", response_description="Admin or User data added into the database")
async def create(adminRequest: admin.AdminRequest):

    return await crud.create_admin(adminRequest)





## function to get all admin and users base on their active status
@admin_router.get("/all")
async def get_all():
    return await crud.get_all()





## function to get admin or users base on id
@admin_router.get("/id/{id}")
async def get_by_id(id: str):
    
    return await crud.getAdminById(id)






## function to update admin or users base on id
@admin_router.put("/update")
async def update(updateAdmin: admin.UpdateAdmin):
   
   return await crud.updateAdmin(updateAdmin)






## function to get admin or user base on email
@admin_router.get("/email/{email}")
async def get_by_email(email: str):
    
    return await crud.get_by_email(email)





## function to get admin or user base on token
@admin_router.get("/token/{token}")
async def get_by_token(token: str):
    
    return await crud.get_by_token(token)





## function to update admin or users base on id after reseting password
@admin_router.put("/reset-password")
async def update(updateAdmin: admin.UpdateAdmin):
   
   return await crud.update_user_after_reset_password(updateAdmin)





## function to delete all admin and users base on id
@admin_router.delete("/delete/{id}")
async def delete(id: str):
    
    return await crud.deleteAdmin(id)
    




## function to get admin or users events base on event id
@admin_router.get("/event_id/{event_id}")
async def get_user_event_by_event_id(event_id: int):
    
    return await crud.get_user_event_by_event_id(event_id)





## function to count all admin and users
@admin_router.get("/count")
async def count_all():

    return await crud.count_all_Admin()
