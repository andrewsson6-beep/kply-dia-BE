
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, insert, select, update
from app.models.institution_model import Institution
from app.models.institutioncontribution_model import InstitutionContribution
from app.schema.contribution_schema import InstitutionContributionCreateSchema
from app.schema.institutions_schema import InstitutionsCreateSchemaBase, InstitutionsInfoSchemaBase
from sqlalchemy.orm import selectinload,noload

class InstitutionDAO:
    """Institutions database operation class"""

    def __init__(self, model):
        self.model = model
    
    async def institutions_list_query(self, db: AsyncSession) -> Institution:
       stmt = (select(self.model))
       result = await db.execute(stmt)
       return result.scalars().all()
    
    async def create_institution(self, db: AsyncSession, institution_data: InstitutionsCreateSchemaBase) -> Institution:
        # Get the highest unique number
        stmt_max = select(func.max(self.model.ins_unique_no))
        result = await db.execute(stmt_max)
        max_unique_no = result.scalar()

        # Start from 1001 if table is empty
        if not max_unique_no:
            new_unique_no = 1001
        else:
            new_unique_no = max_unique_no + 1

        # Generate institution code
        new_code = f"INS-{new_unique_no}"
         # Ensure proper handling of optional parents
      

        stmt = (
            insert(self.model)
            .values(
                # ins_for_id=ins_for_id,
                # ins_par_id=ins_par_id,
                ins_unique_no=new_unique_no,
                ins_code=new_code,
                ins_name=institution_data.insName,
                ins_type=institution_data.insType,
                ins_address=institution_data.insAddress,
                ins_phone=institution_data.insPhone,
                ins_email=institution_data.insEmail,
                ins_website=institution_data.insWebsite,
                ins_head_name=institution_data.insHeadName,
            )
            .returning(self.model)
        )
        result = await db.execute(stmt)
        await db.commit()
        return result.scalar_one()
    

    async def get_institution_with_contributions(self, db: AsyncSession, institution_id: int):
        stmt = (
            select(self.model)
            .options(selectinload(self.model.contributions))
            .where(self.model.ins_id == institution_id, self.model.ins_is_deleted == False)
        )
        result = await db.execute(stmt)
        return result.scalar_one_or_none()
    


    async def create_institution_contribution(self, db: AsyncSession, data: InstitutionContributionCreateSchema) -> InstitutionContribution:
        # Insert new contribution
        stmt = (
            insert(InstitutionContribution)
            .values(
                incon_ins_id=data.institutionId,
                incon_amount=data.amount,
                incon_purpose=data.purpose,
                incon_is_deleted=False,
                incon_date=data.institutionContributionDate
            )
            .returning(InstitutionContribution)
        )
        result = await db.execute(stmt)

        contribution = result.scalar_one()

        # Update institutions's total contribution
        stmt_update = (
            update(Institution)
            .where(Institution.ins_id == data.institutionId)
            .values(ins_total_contribution_amount=Institution.ins_total_contribution_amount + data.amount)
        )
        await db.execute(stmt_update)
        await db.commit()
        return contribution
    

    async def update_institution(self, db: AsyncSession, ins_id: int, update_data: dict) -> Institution | None:
        stmt = (
            update(self.model)
            .where(self.model.ins_id == ins_id, self.model.ins_is_deleted == False)
            .values(**update_data)
            .returning(self.model).options(noload(Institution.contributions))
        )
        result = await db.execute(stmt)
        await db.commit()
        return result.scalar_one_or_none()
    
    async def update_contribution(self, db: AsyncSession, incon_id: int, update_data: dict) -> InstitutionContribution | None:
        # Fetch old contribution first
        stmt_old = select(InstitutionContribution).where(
            InstitutionContribution.incon_id == incon_id,InstitutionContribution.incon_is_deleted == False
        )
        result = await db.execute(stmt_old)
        old_contribution = result.scalar_one_or_none()

        if not old_contribution:
            return None

        old_amount = old_contribution.incon_amount or 0
        new_amount = update_data.get("incon_amount", old_amount)

        # Update contribution row
        stmt = (
            update(InstitutionContribution)
            .where(InstitutionContribution.incon_id == incon_id, InstitutionContribution.incon_is_deleted == False)
            .values(**update_data)
            .returning(InstitutionContribution)
        )
        result = await db.execute(stmt)
        updated_contribution = result.scalar_one_or_none()

        # Adjust Institution total contribution
        diff = new_amount - old_amount
        await db.execute(
            update(Institution)
            .where(Institution.ins_id == old_contribution.incon_ins_id)
            .values(
                ins_total_contribution_amount=Institution.ins_total_contribution_amount + diff
            )
        )

        await db.commit()
        return updated_contribution
    
    async def delete_institution_query(self, db: AsyncSession, user_id: int, institution: int) -> bool:
        """Soft delete individual"""
        stmt = (
            update(self.model)
            .where(self.model.ins_id == institution, self.model.ins_is_deleted == False)
            .values(
                ins_is_deleted=True,
                ins_updated_by=user_id
            )
            .returning(self.model)
        )
        result = await db.execute(stmt)
        await db.commit()
        return result.scalar_one_or_none()

    

    

dao_institutions:InstitutionDAO = InstitutionDAO(Institution)
