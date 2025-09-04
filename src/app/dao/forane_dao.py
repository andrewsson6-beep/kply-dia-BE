from app.models.forane_model import Forane
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.models.systemuser_model import SystemUser


class ForaneDAO:
    """Forane database operation class"""

    def __init__(self, model):
        self.model = model
    
    async def forane_list_query(self, db: AsyncSession) -> Forane:
       stmt = (select(self.model))
       result = await db.execute(stmt)
       return result.scalars()
    

dao_forane:ForaneDAO = ForaneDAO(Forane)





