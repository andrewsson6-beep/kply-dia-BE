
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.individual_model import Individual
class IndividualDAO:
    """Individual database operation class"""

    def __init__(self, model):
        self.model = model
    
    async def individuals_list_query(self, db: AsyncSession) -> Individual:
       stmt = (select(self.model))
       result = await db.execute(stmt)
       return result.scalars()
    

dao_individuals:IndividualDAO = IndividualDAO(Individual)
