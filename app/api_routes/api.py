from fastapi import APIRouter
from routers.admin.endpoint import admin
from routers.events.endpoint import events
from routers.participants.endpoint import participants
from routers.attendances.endpoint import attendances
from routers.participants.endpoint import participantfields


router = APIRouter()
router.include_router(admin.admin_router)
router.include_router(events.events_router)
router.include_router(participants.router)
router.include_router(participantfields.participantfields_router)
