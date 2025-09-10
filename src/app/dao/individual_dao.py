
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, insert, select, update
from app.models.individual_model import Individual
from app.models.individualcontribution_model import IndividualContribution
from app.schema.individuals_schema import IndividualDetailRequestSchema, IndividualsInfoSchemaBase
from app.schema.contribution_schema import IndividualContributionCreateSchema,IndividualContributionResponseSchema
from sqlalchemy.orm import selectinload,noload

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
                ind_total_contribution_amount=0,
            )
            .returning(self.model)
        )
        result = await db.execute(stmt)
        await db.commit()
        return result.scalar_one()
    

    async def create_individuaL_contribution(self, db: AsyncSession, data: IndividualContributionCreateSchema) -> IndividualContribution:
        # Insert new contribution
        stmt = (
            insert(IndividualContribution)
            .values(
                icon_ind_id=data.individualId,
                icon_amount=data.amount,
                icon_purpose=data.purpose,
                icon_is_deleted=False,
            )
            .returning(IndividualContribution)
        )
        result = await db.execute(stmt)

        contribution = result.scalar_one()

        # Update individual's total contribution
        stmt_update = (
            update(Individual)
            .where(Individual.ind_id == data.individualId)
            .values(ind_total_contribution_amount=Individual.ind_total_contribution_amount + data.amount)
        )
        await db.execute(stmt_update)

        await db.commit()
        return contribution
    
    async def get_individual_with_contributions(self, db: AsyncSession, obj:IndividualDetailRequestSchema) -> Individual | None:
        stmt = (
            select(self.model).options(selectinload(Individual.contributions))
            .where(self.model.ind_id == obj.individualId, self.model.ind_is_deleted == False)
        )
        result = await db.execute(stmt)
        await db.flush()
        return result.scalar_one_or_none()
    
    async def update_individual(self, db: AsyncSession, individual_id: int, update_data: dict) -> Individual | None:
        stmt = (
            update(self.model)
            .where(self.model.ind_id == individual_id, self.model.ind_is_deleted == False)
            .values(**update_data)
            .returning(self.model).options(noload(Individual.contributions))
        )
        result = await db.execute(stmt)
        await db.commit()
        return result.scalar_one_or_none()
    
    async def update_contribution(self, db: AsyncSession, contribution_id: int, update_data: dict) -> IndividualContribution | None:
        # Step 1: Get existing contribution
        stmt_old = select(IndividualContribution).where(
            IndividualContribution.icon_id == contribution_id,
            IndividualContribution.icon_is_deleted == False
        )
        result_old = await db.execute(stmt_old)
        old_contribution = result_old.scalar_one_or_none()

        if not old_contribution:
            return None
        



        # Step 2: Apply update and return updated row
        stmt = (
            update(IndividualContribution)
            .where(IndividualContribution.icon_id == contribution_id, IndividualContribution.icon_is_deleted == False)
            .values(**update_data)
            .returning(IndividualContribution)
        )
        result = await db.execute(stmt)
        updated_contribution = result.scalar_one_or_none()

        # Step 3: Adjust individual's total contribution
        if "icon_amount" in update_data:
            # Recalculate total from contributions
            total_stmt = select(func.sum(IndividualContribution.icon_amount)).where(
                IndividualContribution.icon_ind_id == old_contribution.icon_ind_id,
                IndividualContribution.icon_is_deleted == False
            )
            result = await db.execute(total_stmt)
            new_total = result.scalar() or 0

            await db.execute(
                update(Individual)
                .where(Individual.ind_id == old_contribution.icon_ind_id)
                .values(ind_total_contribution_amount=new_total)
            )

        await db.commit()
        return updated_contribution
    

dao_individuals:IndividualDAO = IndividualDAO(Individual)
