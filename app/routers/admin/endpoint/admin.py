from fastapi import APIRouter, Depends
from utils.database import Database
from routers.admin.schemas import admin
from routers.admin.repo import crud
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm



# APIRouter creates path operations for staffs module
admin_router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
    responses={404: {"description": "Not found"}},
)




database = Database()
engine = database.get_db_connection()
session = database.get_db_session(engine)


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")



@admin_router.post('/login', response_model=admin.Token)
async def admin_login(form_data: OAuth2PasswordRequestForm = Depends()):
    
    return await crud.admin_authentication(form_data)







@admin_router.post("/add", response_description="Admin data added into the database")
async def add_admin(adminRequest: admin.AdminRequest):

    return await crud.create_admin(adminRequest)






@admin_router.get("/getAllAdmin")
async def all_admin():
    return await crud.get_all_admin()




@admin_router.get("/getAdminById/{id}")
async def getAdminById(id: str):
    
    return await crud.getAdminById(id)







@admin_router.put("/update")
async def updateAdmin(updateAdmin: admin.UpdateAdmin):
   
   return await crud.updateAdmin(updateAdmin)







@admin_router.get("/getAdminByEmail/{email}")
async def getAdminByEmail(email: str):
    
    return await crud.getAdminByEmail(email)







@admin_router.delete("/delete/{id}")
async def deleteAdmin(id: str):
    
    return await crud.deleteAdmin(id)
    







@admin_router.get("/countAdmin")
async def count_all_Admin():

    return await crud.count_all_Admin()
