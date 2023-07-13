from fastapi import APIRouter, Depends
from utils.database import Database
from routers.admin.schemas import admin
from routers.admin.repo import crud
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm



# APIRouter creates path operations for users module
admin_router = APIRouter(
    prefix="/admin",
    tags=["Admin and Users"],
    responses={404: {"description": "Not found"}},
)




database = Database()
engine = database.get_db_connection()
session = database.get_db_session(engine)


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")



@admin_router.post('/login', response_model=admin.Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    
    return await crud.admin_authentication(form_data)







@admin_router.post("/add", response_description="Admin or User data added into the database")
async def create(adminRequest: admin.AdminRequest):

    return await crud.create_admin(adminRequest)






@admin_router.get("/all")
async def get_all():
    return await crud.get_all_admin()




@admin_router.get("/id/{id}")
async def get_by_id(id: str):
    
    return await crud.getAdminById(id)







@admin_router.put("/update")
async def update(updateAdmin: admin.UpdateAdmin):
   
   return await crud.updateAdmin(updateAdmin)







@admin_router.get("/email/{email}")
async def get_by_email(email: str):
    
    return await crud.get_by_email(email)







@admin_router.delete("/delete/{id}")
async def delete(id: str):
    
    return await crud.deleteAdmin(id)
    







@admin_router.get("/count")
async def count_all():

    return await crud.count_all_Admin()
