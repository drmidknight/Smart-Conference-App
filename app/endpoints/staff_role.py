# from fastapi import APIRouter
# from schemas.schemas import *
# from response.response import Response
# from models.models import Students, Staff_Role
# from db.database import Database
# from sqlalchemy.orm import joinedload



# # APIRouter creates path operations for product module
# router = APIRouter(
#     prefix="/staffRole",
#     tags=["staffRole"],
#     responses={404: {"description": "Not found"}},
# )


# database = Database()
# engine = database.get_db_connection()
# session = database.get_db_session(engine)





# @router.get("/getAllstaffRole")
# async def getAllstaffRole():
#     data = session.query(Staff_Role).all()
#     return Response("ok", "Staff Role retrieved successfully.", data, 200, False)









# @router.patch("/saveStaffRole")
# async def updateStaffRole(updateStaffRoleSchema: UpdateStaffRoleRequest):
#     staffRoleID = updateStaffRoleSchema.id
#     try:
#         is_staffRoleID_update = session.query(Staff_Role).filter(Staff_Role.id == staffRoleID).update({
#             Staff_Role.staff_name: updateStaffRoleSchema.staff_name,
#             Staff_Role.module_start_date: updateStaffRoleSchema.module_start_date,
#             Staff_Role.module_end_date: updateStaffRoleSchema.module_end_date
#         }, synchronize_session=False)
#         session.flush()
#         session.commit()
#         response_msg = "Staff Role updated successfully"
#         response_code = 200
#         error = False
#         if is_staffRoleID_update == 1:
#             # After successful update, retrieve updated data from db
#             data = session.query(Staff_Role).filter(
#                 Staff_Role.id == staffRoleID).one()

#         elif is_staffRoleID_update == 0:
#             response_msg = "Staff Role not updated. No staff role found with this id :" + \
#                 str(staffRoleID)
#             error = True
#             data = None
#         return Response("ok", response_msg, data, response_code, error)
#     except Exception as ex:
#         print("Error : ", ex)









# @router.delete("/deleteCourseById/{id}")
# async def delete_course(id: str):
#     try:
#         is_course_updated = session.query(Course_Batch).filter(Course_Batch.id == id).update({
#             Course_Batch.status: "Inactive"}, synchronize_session=False)
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








# @router.get("/countCourses")
# async def count_all_course():
#     data = session.query(Course_Batch).count()
#     return Response("ok", "count retrieved successfully.", data, 200, False)







# @router.get("/findAllCourseBatchesUnderEachCourse")
# async def findAllCourseBatchesUnderEachCourse(course_id: str):
#     response_message = "Course Batch retrieved successfully"
#     data = None
#     try:
#         data = session.query(Course_Batch).filter(Course_Batch.course_id == course_id).all()
#     except Exception as ex:
#         print("Error", ex)
#         response_message = "Course Batch Not found"
#     error = False
#     return Response("ok", response_message, data, 200, error)








# @router.get("/findStudentCourseBatch")
# async def findStudentCourseBatch(id: str):
#     response_message = "Course Batch retrieved successfully"
#     data = None
#     try:
#         # data = session.query(Course_Batch).options(joinedload(Book.authors)).where(Students.id == id).one()
#         data = session.query(Course_Batch).filter(Course_Batch.id == Students.batch_id).where(Students.id == id).one()
#     except Exception as ex:
#         print("Error", ex)
#         response_message = "Course Batch Not found"
#     error = False
#     return Response("ok", response_message, data, 200, error)







# @router.get("/findModulesUnderEachCourseBatch/")
# async def findModulesUnderEachCourseBatch(id: int):
#     response_message = "Modules retrieved successfully"
#     data = None
#     try:
#         data = session.query(Staff_Role).filter(Staff_Role.batch_id == id).all()
#     except Exception as ex:
#         print("Error", ex)
#         response_message = "Modules Not found"
#     error = False
#     return Response("ok", response_message, data, 200, error)
