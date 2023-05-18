from pydantic import BaseModel, EmailStr, Field
from typing import Optional



class CourseRequest(BaseModel):
    course_name:str

        
class UpdateCourseRequest(BaseModel):
    id:int
    course_name:str









class CourseBatchRequest(BaseModel):
    course_name:str
    course_id:int
    course_level:str
    coordinator:str
    course_start_date:str
    course_end_date:str


class UpdateCourseBatchRequest(BaseModel):
    id:int
    course_name:str
    course_id:int
    course_level:str
    coordinator:str
    course_start_date:str
    course_end_date:str







class ModuleRequest(BaseModel):
    module_name:str
    course_id:int


class UpdateModuleRequest(BaseModel):
    id:int
    module_name:str
    course_id:int








class StudentRequest(BaseModel):
    name:str
    student_id:str
    batch_id:int
    date_of_birth:str
    contact:str
    gender:str
    email:EmailStr = Field(None, title="Staff Email")
    fees:str


class UpdateStudentRequest(BaseModel):
    id:int
    name:Optional[str]
    student_id:Optional[str]
    batch_id:Optional[int]
    date_of_birth:Optional[str]
    contact:Optional[str]
    gender:Optional[str]
    email:Optional[EmailStr] = Field(None, title="Staff Email")
    fees:Optional[str]










class PastStudentRequest(BaseModel):
    no:Optional[int]
    id:int
    name:str
    student_id:str
    batch_id:int
    date_of_birth:str
    contact:str
    gender:str
    email:str
    fees:str







class AdminRequest(BaseModel):
    admin_name:str
    email:EmailStr = Field(None, title="Admin Email")
    contact:str



class UpdateStaffRequest(BaseModel):
    id:Optional[int]
    name:Optional[str]
    contact:Optional[str]
    department:Optional[str]
    batch_id:Optional[int]
    email:Optional[EmailStr] = Field(None, title="Staff Email")
    password:Optional[str]
    reset_password_token:Optional[str]
    usertype:Optional[str]




class UpdateStaffDetailsAfterResetPassword(BaseModel):
    id:Optional[int]
    password:str
    reset_password_token:Optional[str]





class StaffRoleRequest(BaseModel):
    staff_name:str
    course_id:int
    batch_id:int
    module_name:str
    module_start_date:str
    module_end_date:str


class UpdateStaffRoleRequest(BaseModel):
    id:int
    staff_name:str
    module_start_date:str
    module_end_date:str











class UpdateStudentResultsRequest(BaseModel):
    id:int
    marks:Optional[int]
    approval:Optional[bool] = Field(False, description="Value must be either True or False")




class LoginModel(BaseModel):
    email:str
    password:str



class Settings(BaseModel):
    authjwt_secret_key:str='f7ba61299699cb4ca16a09a5ee5fe6aa3db551acf4a5959c1063f7320c13a77e'