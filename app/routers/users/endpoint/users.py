from fastapi import APIRouter, Depends
from utils.database import Database
from routers.users.schemas import users
from routers.users.repo import crud
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm



# APIRouter creates path operations for Users module
users_router = APIRouter(
    prefix="/users",
    tags=["Users"],
    responses={404: {"description": "Not found"}},
)




database = Database()
engine = database.get_db_connection()
session = database.get_db_session(engine)


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")



@users_router.post('/login', response_model=users.Token)
async def admin_login(form_data: OAuth2PasswordRequestForm = Depends()):
    
    return await crud.admin_authentication(form_data)







@users_router.post("/add", response_description="Admin data added into the database")
async def add_admin(adminRequest: admin.AdminRequest):

    return await crud.create_admin(adminRequest)






@users_router.get("/getAllAdmin")
async def all_admin():
    return await crud.get_all_admin()




@users_router.get("/getAdminById/{id}")
async def getAdminById(id: str):
    
    return await crud.getAdminById(id)







@users_router.put("/update")
async def updateAdmin(updateAdmin: admin.UpdateAdmin):
   
   return await crud.updateAdmin(updateAdmin)







@users_router.get("/getAdminByEmail/{email}")
async def getAdminByEmail(email: str):
    
    return await crud.getAdminByEmail(email)







@users_router.delete("/delete/{id}")
async def deleteAdmin(id: str):
    
    return await crud.deleteAdmin(id)
    







@users_router.get("/countAdmin")
async def count_all_Admin():

    return await crud.count_all_Admin()
