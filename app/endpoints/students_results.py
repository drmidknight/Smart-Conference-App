# from fastapi import APIRouter, status
# from schemas.schemas import UpdateStudentResultsRequest
# from response.response import Response
# from models.models import Students, Past_Students, Students_Results
# from db.database import Database
# from sqlalchemy import and_, or_
# from fastapi.exceptions import HTTPException



# # APIRouter creates path operations for product module
# router = APIRouter(
#     prefix="/studentResults",
#     tags=["studentResults"],
#     responses={404: {"description": "Not found"}},
# )


# database = Database()
# engine = database.get_db_connection()
# session = database.get_db_session(engine)





# @router.get("/getAllStudent")
# async def all_students():
#     data = session.query(Students_Results).all()
#     return Response("ok", "Student retrieved successfully.", data, 200, False)





# @router.patch("/saveStudentResults")
# async def saveStudentResults(saveStudentResults: UpdateStudentResultsRequest):
#     studendResults = saveStudentResults.id
#     try:
#         is_studendResults_update = session.query(Students_Results).filter(Students_Results.id == studendResults).update({
#             Students_Results.marks: saveStudentResults.marks,
#             Students_Results.approval: saveStudentResults.approval
#         }, synchronize_session=False)
#         session.flush()
#         session.commit()
#         response_msg = "Student Results updated successfully"
#         response_code = 200
#         error = False
#         if is_studendResults_update == 1:
#             # After successful update, retrieve updated data from db
#             data = session.query(Students_Results).filter(
#                 Students_Results.id == studendResults).one()

#         elif is_studendResults_update == 0:
#             response_msg = "Student Results not updated. No Student Results found with this id :" + \
#                 str(studendResults)
#             error = True
#             data = None
#         return Response("ok", response_msg, data, response_code, error)
#     except Exception as ex:
#         print("Error : ", ex)










# @router.get("/findAllStudentsUnderResultsByModuleName")
# async def findAllStudentsUnderResultsByModuleName(module_name: str):
#     response_message = "Students retrieved successfully"
#     data = None
#     try:
#         data = session.query(Students_Results).filter(Students_Results.module_name == module_name).all()
#     except Exception as ex:
#         print("Error", ex)
#         response_message = "Students Not found"
#     error = False
#     return Response("ok", response_message, data, 200, error)








# @router.get("/findStudentResultsByStudentIdAndCourseId")
# async def findStudentResultsByStudentIdAndCourseId(student_id: str, batch_id: int):
#     data = session.query(Students_Results).filter(and_(
#             Students_Results.student_id == Students.student_id,
#             Students_Results.batch_id == Students.batch_id,
#             Students.student_id == student_id,
#             Students.batch_id == batch_id, 
#             Students_Results.approval == 1
#         )).first()
    
#     if data is not None:
#         response_message = "Student Results retrieved successfully"
#         response_code = status.HTTP_200_OK
#         return Response("ok", response_message, data, response_code, False)

#     return HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#             detail="Student Results not found"
#         )








# @router.get("/findPastStudentResultsByStudentIDandCourseID")
# async def findPastStudentResultsByStudentIDandCourseID(student_id: str, batch_id: int):
#     data = session.query(Students_Results).filter(and_(
#         Students_Results.student_id == Past_Students.student_id,
#         Students_Results.batch_id == Past_Students.batch_id,
#         Past_Students.student_id == student_id,
#         Past_Students.batch_id == batch_id, 
#         Students_Results.approval == 1
#         )).first()
    
#     if data is not None:
#         response_message = "Student Results retrieved successfully"
#         response_code = status.HTTP_200_OK
#         return Response("ok", response_message, data, response_code, False)

#     return HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#             detail="Student Results not found"
#         )
