
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.individual_model import Individual
class IndividualDAO:
    """Individual database operation class"""

    def __init__(self, model):
        self.model = model
    
    async def individuals_list_query(self, db: AsyncSession) -> Individual:
       print("--------------At DAO Level Before")
       stmt = (select(self.model))
       result = await db.execute(stmt)
       print("--------------At DAO Level After")
       return result.scalars()
    

dao_individuals:IndividualDAO = IndividualDAO(Individual)
