from fastapi import APIRouter
from app.endpoints import admin


router = APIRouter()
router.include_router(admin.router)
# router.include_router(courses.router)
# router.include_router(modules.router)
# router.include_router(past_students.router)
# router.include_router(staff_details.router)
# router.include_router(staff_role.router)
# router.include_router(students_results.router)
# router.include_router(students.router)