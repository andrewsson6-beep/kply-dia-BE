from fastapi import APIRouter 
from app.api.auth_api import router as authRoute
from app.api.forane_api import router as foraneRoute
from app.api.individual_api import router as individualsRoute
from app.api.institution_api import router as institutionRoute
from app.api.parish_api import router as parishRoute
from app.api.community_api import router as communityRoute
from app.api.family_api import router as familyRoute

router = APIRouter()
router.include_router(authRoute)
router.include_router(foraneRoute)
router.include_router(individualsRoute,prefix='/individual')
router.include_router(institutionRoute,prefix='/institution')
router.include_router(parishRoute)
router.include_router(communityRoute)
router.include_router(familyRoute)