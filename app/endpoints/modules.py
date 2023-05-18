# from fastapi import APIRouter, status
# from schemas.schemas import *
# from response.response import Response
# from models.models import Modules, Courses
# from db.database import Database
# from fastapi.exceptions import HTTPException



# # APIRouter creates path operations for product module
# router = APIRouter(
#     prefix="/modules",
#     tags=["modules"],
#     responses={404: {"description": "Not found"}},
# )


# database = Database()
# engine = database.get_db_connection()
# session = database.get_db_session(engine)





# @router.get("/getAllModules")
# async def all_modules():
#     data = session.query(Modules).filter(Modules.status == "Active").all()
#     return Response("ok", "Modules retrieved successfully.", data, 200, False)








# @router.post("/saveModules", response_description="Modules data added into the database")
# async def add_module(moduleSchema: ModuleRequest):

#     response_code = 200
#     db_module_name = session.query(Modules).filter(Modules.module_name == moduleSchema.module_name).first()

#     if db_module_name is not None:
#         response_msg = str(moduleSchema.module_name) + " already exists"
#         error = True
#         status = "Error"
#         data = None
#         return Response(status, response_msg, data, response_code, error)
    
    
#     new_module = Modules()
#     new_module.module_name = moduleSchema.module_name
#     new_module.course_id = moduleSchema.course_id
#     new_module.status = "Active"
#     session.add(new_module)
#     session.flush()
#     # get id of the inserted product
#     session.refresh(new_module, attribute_names=['id'])
#     data = {"module_name": new_module.module_name}
#     session.commit()
#     session.close()
#     return Response("ok", "Modules added successfully", data, 200, False)
    





# @router.get("/findModuleById/")
# async def read_findModule(id: str):
#     response_message = "Module retrieved successfully"
#     data = None
#     try:
#         data = session.query(Modules).filter(Modules.id == id).one()
#     except Exception as ex:
#         print("Error", ex)
#         response_message = "Module Not found"
#     error = False
#     return Response(data, 200, response_message, error)








# @router.put("/updateCourse")
# async def update_course(update_course: UpdateCourseRequest):
#     course_id = update_course.id
#     try:
#         is_course_update = session.query(Modules).filter(Modules.id == course_id).update({
#             Modules.course_name: update_course.course_name
#         }, synchronize_session=False)
#         session.flush()
#         session.commit()
#         response_msg = "Course updated successfully"
#         response_code = 200
#         error = False
#         if is_course_update == 1:
#             # After successful update, retrieve updated data from db
#             data = session.query(Modules).filter(
#                 Modules.id == course_id).one()

#         elif is_course_update == 0:
#             response_msg = "Course not updated. No course found with this id :" + \
#                 str(course_id)
#             error = True
#             data = None
#         return Response(data, response_code, response_msg, error)
#     except Exception as ex:
#         print("Error : ", ex)










# @router.delete("/deleteCourseById/{id}")
# async def delete_course(id: str):
#     try:
#         is_course_updated = session.query(Modules).filter(Modules.id == id).update({
#             Modules.status: "Inactive"}, synchronize_session=False)
#         session.flush()
#         session.commit()
#         response_msg = "Course deleted successfully"
#         response_code = 200
#         error = False
#         data = {"id": id}
#         if is_course_updated == 0:
#             response_msg = "Course not deleted. No Course found with this id :" + \
#                 str(id)
#             error = True
#             data = None
#         return Response(data, response_code, response_msg, error)
#     except Exception as ex:
#         print("Error : ", ex)








# @router.get("/countModule")
# async def count_all_course():
#     data = session.query(Modules).count()
#     return Response("ok", "count retrieved successfully.", data, 200, False)



# @router.get("/findModulesUnderEachCourse")
# async def findModulesUnderEachCourse(id: int):
#     data = session.query(Modules).filter(Modules.course_id == id).all()
        
#     if data is not None:
#         response_message = "Modules retrieved successfully"
#         response_code = status.HTTP_200_OK
#         return Response("ok", response_message, data, response_code, False)

#     return HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#             detail="Module not found"
#         )

    






