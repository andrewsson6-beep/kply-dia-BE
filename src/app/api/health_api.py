from fastapi import APIRouter, Depends
from sqlalchemy import text

from common.google.scheduler_auth import verify_cloud_scheduler_oidc
from database.db import async_db_session

router = APIRouter()


@router.get(
    "/db-health",
    response_model=bool,
    dependencies=[Depends(verify_cloud_scheduler_oidc)],
)
async def db_health() -> bool:
    try:
        async with async_db_session() as db:
            await db.execute(text("SELECT 1"))
        return True
    except Exception:
        return False
