
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, insert, select
from app.models.individual_model import Individual
from app.schema.individuals_schema import IndividualsInfoSchemaBase

class IndividualDAO:
    """Individual database operation class"""

    def __init__(self, model):
        self.model = model
    
    async def individuals_list_query(self, db: AsyncSession) -> Individual:
       stmt = (select(self.model))
       result = await db.execute(stmt)
       return result.scalars().all()
    
    async def create_individual(self, db: AsyncSession, individual_data: IndividualsInfoSchemaBase) -> Individual:
        # Get max unique number
        stmt_max = select(func.max(self.model.ind_unique_no))
        result = await db.execute(stmt_max)
        max_unique_no = result.scalar()

        # Start at 1001
        if not max_unique_no:
            new_unique_no = 1001
        else:
            new_unique_no = max_unique_no + 1

        # Generate individual code
        new_code = f"IND-{new_unique_no}"

        stmt = (
            insert(self.model)
            .values(
                ind_unique_no=new_unique_no,
                ind_code=new_code,
                ind_full_name=individual_data.indFullName,
                ind_phone_number=individual_data.indPhoneNumber,
                ind_email=individual_data.indEmail,
                ind_address=individual_data.indAddress,
                ind_total_contribution_amount=individual_data.indContributionAmount,
            )
            .returning(self.model)
        )
        result = await db.execute(stmt)
        await db.commit()
        return result.scalar_one()
    

dao_individuals:IndividualDAO = IndividualDAO(Individual)
