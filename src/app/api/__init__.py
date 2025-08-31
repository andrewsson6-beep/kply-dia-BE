from fastapi import APIRouter 
from app.api.auth_api import router as authRoute

router = APIRouter()
router.include_router(authRoute)
