from fastapi import APIRouter
from app.routers.admin.endpoint import admin
from app.routers.events.endpoint import events
from app.routers.participants.endpoint import participants
from app.routers.attendances.endpoint import attendances


router = APIRouter()
router.include_router(admin.admin_router)
router.include_router(events.events_router)
router.include_router(participants.router)
