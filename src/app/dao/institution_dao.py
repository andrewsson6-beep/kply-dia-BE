
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.institution_model import Institution
class InstitutionDAO:
    """Institutions database operation class"""

    def __init__(self, model):
        self.model = model
    
    async def institutions_list_query(self, db: AsyncSession) -> Institution:
       print("--------------At DAO Level Before")
       stmt = (select(self.model))
       result = await db.execute(stmt)
       print("--------------At DAO Level After")
       return result.scalars()
    

dao_institutions:InstitutionDAO = InstitutionDAO(Institution)
