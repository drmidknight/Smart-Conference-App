from routers.participants.endpoint import participantfields
from routers.participants.endpoint import participants
from routers.attendances.endpoint import attendances
from routers.events.endpoint import events
from routers.admin.endpoint import admin
from fastapi import APIRouter









router = APIRouter()
router.include_router(admin.admin_router)
router.include_router(events.events_router)
router.include_router(participants.router)
router.include_router(participantfields.participantfields_router)
