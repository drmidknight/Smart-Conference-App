# from fastapi import APIRouter
# from schemas.schemas import *
# from response.response import Response
# from models.models import Past_Students
# from db.database import Database



# # APIRouter creates path operations for product module
# router = APIRouter(
#     prefix="/pastStudents",
#     tags=["pastStudents"],
#     responses={404: {"description": "Not found"}},
# )


# database = Database()
# engine = database.get_db_connection()
# session = database.get_db_session(engine)





# @router.get("/getAllCourses")
# async def all_courses():
#     data = session.query(Past_Students).all()
#     return Response("ok", "Course retrieved successfully.", data, 200, False)








# @router.post("/saveCourses", response_description="Course data added into the database")
# async def add_course(courseSchema: CourseRequest):

#     response_code = 200
#     db_course_name = session.query(Past_Students).filter(Past_Students.course_name == courseSchema.course_name).first()

#     if db_course_name is not None:
#         response_msg = str(courseSchema.course_name) + " already exists"
#         error = True
#         data = None
#         return Response(data, response_code, response_msg, error)
    
#     new_course = Past_Students()
#     new_course.course_name = courseSchema.course_name
#     new_course.status = "Active"
#     session.add(new_course)
#     session.flush()
#     # get id of the inserted product
#     session.refresh(new_course, attribute_names=['id'])
#     data = {"course_name": new_course.course_name}
#     session.commit()
#     session.close()
#     return Response(data, 200, "Course added successfully.", False)





# @router.get("/retrievingOnlyPastStudentStudentID")
# async def findPastStudentByID(id: str):
#     response_message = "Past Student retrieved successfully"
#     data = None
#     try:
#         data = session.query(Past_Students).filter(Past_Students.id == id).where(Past_Students.id == id).all()
#     except Exception as ex:
#         print("Error", ex)
#         response_message = "Past Student Not found"
#     error = False
#     return Response("ok", response_message, data, 200, error)








# @router.put("/updateCourse")
# async def update_course(update_course: UpdateCourseRequest):
#     course_id = update_course.id
#     try:
#         is_course_update = session.query(Past_Students).filter(Past_Students.id == course_id).update({
#             Past_Students.course_name: update_course.course_name
#         }, synchronize_session=False)
#         session.flush()
#         session.commit()
#         response_msg = "Course updated successfully"
#         response_code = 200
#         error = False
#         if is_course_update == 1:
#             # After successful update, retrieve updated data from db
#             data = session.query(Past_Students).filter(
#                 Past_Students.id == course_id).one()

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
#         is_course_updated = session.query(Past_Students).filter(Past_Students.id == id).update({
#             Past_Students.status: "Inactive"}, synchronize_session=False)
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
#     data = session.query(Past_Students).count()
#     return Response("ok", "count retrieved successfully.", data, 200, False)







