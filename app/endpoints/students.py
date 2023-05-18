# from fastapi import APIRouter, status
# from schemas.schemas import StudentRequest,UpdateStudentRequest
# from response.response import Response
# from models.models import Students, Modules, Students_Results
# from db.database import Database
# from sqlalchemy import and_, or_
# from fastapi.exceptions import HTTPException



# # APIRouter creates path operations for product module
# router = APIRouter(
#     prefix="/students",
#     tags=["students"],
#     responses={404: {"description": "Not found"}},
# )


# database = Database()
# engine = database.get_db_connection()
# session = database.get_db_session(engine)





# @router.get("/getAllStudent")
# async def all_students():
#     data = session.query(Students).all()
#     return Response("ok", "Student retrieved successfully.", data, 200, False)








# @router.post("/saveStudent", response_description="Student data added into the database")
# async def saveStudent(studentRequest: StudentRequest):

#     response_code = 201
#     db_email_contact = session.query(Students).filter(or_(
#         Students.email == studentRequest.email,
#         Students.contact == studentRequest.contact,
#         Students.student_id == studentRequest.student_id
#         )).first()

#     if db_email_contact is not None:
#         response_msg =str(studentRequest.name) + " email " + str(studentRequest.email) + " already exists"
#         error = True
#         data = None
#         return Response("ok", response_msg, data, response_code, error)

#     new_student = Students()
#     new_student.name = studentRequest.name
#     new_student.student_id = studentRequest.student_id
#     new_student.batch_id = studentRequest.batch_id
#     new_student.date_of_birth = studentRequest.date_of_birth
#     new_student.contact = studentRequest.contact
#     new_student.gender = studentRequest.gender
#     new_student.email = studentRequest.email
#     new_student.fees = studentRequest.fees
#     new_student.status = "Active"
#     session.add(new_student)
#     session.flush()
#     # get id of the inserted product
#     session.refresh(new_student, attribute_names=['id'])
#     data = {"student_name": new_student.name}
#     session.commit()
#     session.close()
#     return Response("ok", "Student added successfully.", data, 200, False)





# @router.get("/findCourseById/{id}")
# async def read_findcourse(id: str):
#     response_message = "Course retrieved successfully"
#     data = None
#     try:
#         data = session.query(Students).filter(Students.id == id).one()
#     except Exception as ex:
#         print("Error", ex)
#         response_message = "Course Not found"
#     error = False
#     return Response(data, 200, response_message, error)








# @router.patch("/updateStudent")
# async def updateStudent(updateStudent: UpdateStudentRequest):
#     student_id = updateStudent.id
#     try:
#         is_student_update = session.query(Students).filter(Students.id == student_id).update({
#             Students.student_id: updateStudent.student_id,
#             Students.batch_id: updateStudent.batch_id,
#             Students.name: updateStudent.name,
#             Students.date_of_birth: updateStudent.date_of_birth,
#             Students.contact: updateStudent.contact,
#             Students.email: updateStudent.email,
#             Students.fees: updateStudent.fees
#         }, synchronize_session=False)
#         session.flush()
#         session.commit()
#         response_msg = "Student updated successfully"
#         response_code = 200
#         error = False
#         if is_student_update == 1:
#             # After successful update, retrieve updated data from db
#             data = session.query(Students).filter(
#                 Students.id == student_id).one()

#         elif is_student_update == 0:
#             response_msg = "Student not updated. No Student found with this id :" + \
#                 str(student_id)
#             error = True
#             data = None
#         return Response("ok", response_msg, data, response_code, error)
#     except Exception as ex:
#         print("Error : ", ex)










# @router.delete("/deleteCourseById/{id}")
# async def delete_course(id: str):
#     try:
#         is_course_updated = session.query(Students).filter(Students.id == id).update({
#             Students.status: "Inactive"}, synchronize_session=False)
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








# @router.get("/countStudent")
# async def count_all_student():
#     data = session.query(Students).count()
#     return Response("ok", "Student retrieved successfully.", data, 200, False)







# @router.get("/findStudentsUnderModule")
# async def findStudentsUnderModule(id: int):
#     data = session.query(Students).filter(Modules.id == id).all()
    
#     if data is not None:
#         response_message = "Student retrieved successfully"
#         response_code = status.HTTP_200_OK
#         return Response("ok", response_message, data, response_code, False)

#     return HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#             detail="Student not found"
#         )






# @router.get("/findStudentsUnderCourseBatch")
# async def findStudentsUnderCourseBatch(id: int):
#     data = session.query(Students).filter(Students.batch_id == id).all()
        
#     if data is not None:
#         response_message = "Student retrieved successfully"
#         response_code = status.HTTP_200_OK
#         return Response("ok", response_message, data, response_code, False)

#     return HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#             detail="Student not found"
#         )






# @router.get("/selectingFromStudentForResults")
# async def selectingFromStudentForResults(student_id: str, batch_id: int):

#     data = session.query(Students).filter(and_(
#             Students_Results.student_id == Students.student_id,
#             Students_Results.batch_id == Students.batch_id,
#             Students.student_id == student_id,
#             Students.batch_id == batch_id
#         )).first()
    
#     if data is not None:
#         response_message = "Student retrieved successfully"
#         response_code = status.HTTP_200_OK
#         return Response("ok", response_message, data, response_code, False)

#     return HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#             detail="Student not found"
#         )

#     # response_msg = "Student with ID (" + \
#     # str(student_id) + ") not found"
#     # response_code = status.HTTP_404_NOT_FOUND
#     # data = None
#     # return Response("ok", response_msg, data, response_code, True)
    