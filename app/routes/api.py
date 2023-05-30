from fastapi import APIRouter
from app.services.admin.endpoint import admin
from app.services.events.endpoint import events
from app.services.participants.endpoint import participants
from app.services.attendances.endpoint import attendances


router = APIRouter()
router.include_router(admin.admin_router)
router.include_router(events.events_router)
router.include_router(participants.router)
# router.include_router(past_students.router)
# router.include_router(staff_details.router)
# router.include_router(staff_role.router)
# router.include_router(students_results.router)
# router.include_router(students.router)