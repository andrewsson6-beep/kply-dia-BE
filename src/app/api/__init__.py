from fastapi import APIRouter 
from app.api.auth_api import router as authRoute
from app.api.forane_api import router as foraneRoute
from app.api.individual_api import router as individualsRoute
from app.api.institution_api import router as institutionRoute
from app.api.parish_api import router as parishRoute

router = APIRouter()
router.include_router(authRoute)
router.include_router(foraneRoute)
router.include_router(individualsRoute)
router.include_router(institutionRoute)
router.include_router(parishRoute)