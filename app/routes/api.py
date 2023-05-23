from fastapi import APIRouter
from app.endpoints import admin, events, participants, attendances


router = APIRouter()
router.include_router(admin.router)
router.include_router(events.router)
router.include_router(participants.router)
# router.include_router(past_students.router)
# router.include_router(staff_details.router)
# router.include_router(staff_role.router)
# router.include_router(students_results.router)
# router.include_router(students.router)