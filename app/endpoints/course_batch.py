# from fastapi import APIRouter, status, Depends
# from schemas.schemas import *
# from response.response import Response
# from models.models import Course_Batch, Past_Students, Students, Staff_Role, Staff_Details, Students_Results
# from db.database import Database
# from sqlalchemy.orm import joinedload
# from sqlalchemy import and_, desc
# from fastapi.exceptions import HTTPException
# from fastapi_jwt_auth import AuthJWT



# # APIRouter creates path operations for product module
# router = APIRouter(
#     prefix="/courseBatch",
#     tags=["courseBatch"],
#     responses={404: {"description": "Not found"}},
# )


# database = Database()
# engine = database.get_db_connection()
# session = database.get_db_session(engine)





# @router.get("/getAllCourseBatches")
# async def all_coursesBatches(Authorize:AuthJWT=Depends()):
#     data = session.query(Course_Batch).all()
#     return Response("ok", "Course retrieved successfully.", data, 200, False)









# @router.post("/saveCourseBatch", response_description="Course Batch data added into the database")
# async def add_course(courseBatchSchema: CourseBatchRequest):

#     new_courseBatch = Course_Batch()
#     new_courseBatch.course_name = courseBatchSchema.course_name
#     new_courseBatch.course_id = courseBatchSchema.course_id
#     new_courseBatch.course_level = courseBatchSchema.course_level
#     new_courseBatch.coordinator = courseBatchSchema.coordinator
#     new_courseBatch.course_start_date = courseBatchSchema.course_start_date
#     new_courseBatch.course_end_date = courseBatchSchema.course_end_date
#     new_courseBatch.status = "Active"
#     session.add(new_courseBatch)
#     session.flush()
#     # get id of the inserted product
#     session.refresh(new_courseBatch, attribute_names=['id'])
#     data = {"course_name": new_courseBatch.course_name}
#     session.commit()
#     session.close()
#     return Response("ok", "Course Batch added successfully", data, 200, False)






# @router.get("/findCourseBatchById")
# async def findCourseBatchById(id: str):
#     response_message = "Course Batch retrieved successfully"
#     data = None
#     try:
#         data = session.query(Course_Batch).filter(Course_Batch.id == id).all()
#     except Exception as ex:
#         print("Error", ex)
#         response_message = "Course Batch Not found"
#     error = False
#     return Response("ok", response_message, data, 200, error)








# @router.put("/updateCourse")
# async def update_course(update_course: UpdateCourseRequest):
#     course_id = update_course.id
#     try:
#         is_course_update = session.query(Course_Batch).filter(Course_Batch.id == course_id).update({
#             Course_Batch.course_name: update_course.course_name
#         }, synchronize_session=False)
#         session.flush()
#         session.commit()
#         response_msg = "Course updated successfully"
#         response_code = 200
#         error = False
#         if is_course_update == 1:
#             # After successful update, retrieve updated data from db
#             data = session.query(Course_Batch).filter(
#                 Course_Batch.id == course_id).one()

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
#     data = session.query(Course_Batch).filter(Course_Batch.course_id == course_id).all()
        
#     if data is not None:
#         response_message = "Course Batch retrieved successfully"
#         response_code = status.HTTP_200_OK
#         return Response("ok", response_message, data, response_code, False)
    
#     return HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#             detail="Course Batch not found"
#         )








# @router.get("/findStudentCourseBatch")
# async def findStudentCourseBatch(id: str):
#     data = session.query(Course_Batch).filter(and_(
#             Course_Batch.id == Students.batch_id, 
#             Students.id == id
#             )).all()
    
#     if data is not None:
#         response_message = "Course Batch retrieved successfully"
#         response_code = status.HTTP_200_OK
#         return Response("ok", response_message, data, response_code, False)
    
#     return HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#             detail="Course Batch not found"
#         )









# @router.get("/findPastStudentCourseBatch")
# async def findPastStudentCourseBatch(student_id: str):
#     data = session.query(Course_Batch).filter(and_(
#             Course_Batch.id == Past_Students.batch_id, 
#             Past_Students.id == student_id
#             )).all()
    
#     if data is not None:
#         response_message = "Course Batch retrieved successfully"
#         response_code = status.HTTP_200_OK
#         return Response("ok", response_message, data, response_code, False)
    
#     return HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#             detail="Course Batch not found"
#         )





# @router.get("/findModulesUnderEachCourseBatch")
# async def findModulesUnderEachCourseBatch(id: int):
#     data = session.query(Staff_Role).filter(Staff_Role.batch_id == id).all()
    
#     if data is not None:
#         response_message = "Modules retrieved successfully"
#         response_code = status.HTTP_200_OK
#         return Response("ok", response_message, data, response_code, False)

#     return HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#             detail="Module not found"
#         )







# @router.get("/findStaffCourseBatch")
# async def findStaffCourseBatch(staff_id: int):
#     data = session.query(Course_Batch).filter(and_(
#             Course_Batch.coordinator == Staff_Details.name, 
#             Staff_Details.id == staff_id
#             )).all()

#     if data is not None:
#          response_message = "Course Batch retrieved successfully"
#          response_code = status.HTTP_200_OK
#          return Response("ok", response_message, data, response_code, False)
    
#     return HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#             detail="Course Batch not found"
#         )





# @router.get("/selectingFromCourseBatchForStudentResults")
# async def selectingFromCourseBatchForStudentResults(student_id: str, batch_id: int):
#     data = session.query(Course_Batch).filter(and_(
#             Course_Batch.id == Students.batch_id,
#             Students.student_id == student_id,
#             Students.batch_id == batch_id
#         )).first()
    
#     if data is not None:
#         response_message = "Course retrieved successfully"
#         response_code = status.HTTP_200_OK
#         return Response("ok", response_message, data, response_code, False)

#     return HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#             detail="Course Batch not found"
#         )
        