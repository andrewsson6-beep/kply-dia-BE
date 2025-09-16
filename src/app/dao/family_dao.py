
from sqlalchemy import func, insert, select, update
from app.models.community_model import Community
from app.models.family_model import Family
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.familycontribution_model import FamilyContribution
from app.models.forane_model import Forane
from app.models.parish_model import Parish
from app.schema.contribution_schema import FamilContributionCreateSchema, FamilContributionUpdateSchema
from app.schema.family_schema import FamilyCreateSchema
from sqlalchemy.orm import noload,selectinload


class FamilyDAO:
    """Family Dao Class Operation"""

    def __init__(self, model):
        self.model = model
    
    async def create_family(self, db: AsyncSession, user_id: int, family_data: FamilyCreateSchema) -> Family:
        # Generate unique number
        stmt_max = select(func.max(self.model.fam_unique_no))
        result = await db.execute(stmt_max)
        max_unique_no = result.scalar() or 0
        new_unique_no = max_unique_no + 1

        # Generate family code
        new_code = f"FAM-{new_unique_no:04d}"

        stmt = (
            insert(self.model)
            .values(
                fam_com_id=family_data.fam_com_id,
                fam_unique_no=new_unique_no,
                fam_code=new_code,
                fam_house_name=family_data.fam_house_name,
                fam_head_name=family_data.fam_head_name,
                fam_phone_number=family_data.fam_phone_number,
                fam_total_contribution_amount=0,
                fam_is_deleted=False,
                fam_created_by=user_id,
            )
            .returning(self.model)
        )
        result = await db.execute(stmt)
        await db.commit()
        return result.scalar_one()
    

    async def update_family(self, db: AsyncSession, family_id: int, update_data: dict) -> Family | None:
        stmt = (
            update(self.model)
            .where(self.model.fam_id == family_id, self.model.fam_is_deleted == False)
            .values(**update_data)
            .returning(self.model)
        )
        result = await db.execute(stmt)
        await db.commit()
        return result.scalar_one_or_none()
    

    
    async def create_family_contribution(self, db: AsyncSession, user_id: int, data: FamilContributionCreateSchema) -> FamilyContribution | None:
        """
        Create a new family contribution and cascade update totals
        for Family -> Community -> Parish/Forane.
        """

        # 1. Insert new contribution
        stmt = (
            insert(FamilyContribution)
            .values(
                fcon_fam_id=data.familyId,
                fcon_amount=data.amount,
                fcon_purpose=data.purpose,
                fcon_is_deleted=False,
                fcon_created_by=user_id,
                fcon_updated_by=user_id,
            )
            .returning(FamilyContribution)
            .options(noload(FamilyContribution.family))
        )
        result = await db.execute(stmt)
        contribution = result.scalar_one()

        # 2. Update Family total
        stmt_update_family = (
            update(Family)
            .where(Family.fam_id == data.familyId)
            .values(
                fam_total_contribution_amount=Family.fam_total_contribution_amount + data.amount,
                fam_updated_by=user_id,
            )
        )
        await db.execute(stmt_update_family)

        # 3. Fetch Community, Parish, Forane in ONE query
        q = (
            select(
                Community.com_id,
                Community.com_for_id,
                Community.com_par_id,
                Parish.par_for_id,
            )
            .join(Family, Family.fam_com_id == Community.com_id)
            .outerjoin(Parish, Parish.par_id == Community.com_par_id)
            .where(Family.fam_id == data.familyId)
        )
        res = await db.execute(q)
        com_id, com_for_id, com_par_id, par_for_id = res.one_or_none()

        # 4. Update Community
        stmt_update_com = (
            update(Community)
            .where(Community.com_id == com_id)
            .values(
                com_total_contribution_amount=Community.com_total_contribution_amount + data.amount,
                com_updated_by=user_id,
            )
        )
        await db.execute(stmt_update_com)

        # 5. If Community is directly under Forane
        if com_for_id and not com_par_id:
            stmt_update_forane = (
                update(Forane)
                .where(Forane.for_id == com_for_id)
                .values(
                    for_total_contribution_amount=Forane.for_total_contribution_amount + data.amount,
                    for_updated_by=user_id,
                )
            )
            await db.execute(stmt_update_forane)

        # 6. If Community belongs to Parish
        elif com_par_id:
            stmt_update_parish = (
                update(Parish)
                .where(Parish.par_id == com_par_id)
                .values(
                    par_total_contribution_amount=Parish.par_total_contribution_amount + data.amount,
                    par_updated_by=user_id,
                )
            )
            await db.execute(stmt_update_parish)

            if par_for_id:
                stmt_update_forane = (
                    update(Forane)
                    .where(Forane.for_id == par_for_id)
                    .values(
                        for_total_contribution_amount=Forane.for_total_contribution_amount + data.amount,
                        for_updated_by=user_id,
                    )
                )
                await db.execute(stmt_update_forane)

        # 7. Commit
        await db.commit()

        return contribution



    


    
    async def get_family_with_contributions(self, db: AsyncSession,fam_id:int) -> Family | None: 
        stmt = (
            select(self.model).options(selectinload(Family.contributions))
            .where(self.model.fam_id == fam_id, self.model.fam_is_deleted == False)
        )
        result = await db.execute(stmt)
        await db.flush()
        return result.scalar_one_or_none()
    

    # async def update_family_contribution(self, db: AsyncSession, user_id: int, fcon_id: int, data: FamilContributionUpdateSchema) -> FamilyContribution | None:
    #     """Update an existing family contribution"""

    #     # 1. Get old contribution
    #     q = select(FamilyContribution).where(FamilyContribution.fcon_id == fcon_id)
    #     res = await db.execute(q)
    #     contribution = res.scalar_one_or_none()
    #     if not contribution:
    #         return None

    #     old_amount = contribution.fcon_amount
    #     new_amount = data.amount
    #     delta = new_amount - old_amount

    #     # 2. Update FamilyContribution record
    #     stmt = (
    #         update(FamilyContribution)
    #         .where(FamilyContribution.fcon_id == fcon_id)
    #         .values(
    #             fcon_amount=new_amount,
    #             fcon_purpose=data.purpose,
    #             fcon_updated_by=user_id,
    #         )
    #         .returning(FamilyContribution).options(noload(FamilyContribution.family))
    #     )
    #     result = await db.execute(stmt)
    #     updated_contribution = result.scalar_one()

    #     # 3. Cascade updates (if delta != 0)
    #     if delta != 0:
    #         await self._cascade_update_totals(db, updated_contribution.fcon_fam_id, delta, user_id)

    #     await db.commit()
    #     return updated_contribution
    
    # async def delete_family_contribution(self, db: AsyncSession, user_id: int, fcon_id: int) -> bool:
    #     """Soft delete a family contribution"""

    #     # 1. Get contribution
    #     q = select(FamilyContribution).where(FamilyContribution.fcon_id == fcon_id)
    #     res = await db.execute(q)
    #     contribution = res.scalar_one_or_none()
    #     if not contribution or contribution.fcon_is_deleted:
    #         return False

    #     amount = contribution.fcon_amount

    #     # 2. Mark as deleted
    #     stmt = (
    #         update(FamilyContribution)
    #         .where(FamilyContribution.fcon_id == fcon_id)
    #         .values(
    #             fcon_is_deleted=True,
    #             fcon_updated_by=user_id,
    #         )
    #     )
    #     await db.execute(stmt)

    #     # 3. Cascade update (subtract the amount)
    #     await self._cascade_update_totals(db, contribution.fcon_fam_id, -amount, user_id)

    #     await db.commit()
    #     return True
    


    # async def _cascade_update_totals(self, db: AsyncSession, family_id: int, delta: float, user_id: int):
    #     """Update Family, Community, Parish, Forane totals based on contribution delta"""

    #     # Get hierarchy
    #     q = (
    #         select(Family.fam_com_id, Community.com_par_id, Community.com_for_id)
    #         .join(Community, Community.com_id == Family.fam_com_id)
    #         .where(Family.fam_id == family_id)
    #     )
    #     res = await db.execute(q)
    #     row = res.one_or_none()
    #     if not row:
    #         return
    #     com_id, par_id, for_id = row

    #     # Family
    #     await db.execute(
    #         update(Family)
    #         .where(Family.fam_id == family_id)
    #         .values(
    #             fam_total_contribution_amount=Family.fam_total_contribution_amount + delta,
    #             fam_updated_by=user_id,
    #         )
    #     )

    #     # Community
    #     await db.execute(
    #         update(Community)
    #         .where(Community.com_id == com_id)
    #         .values(
    #             com_total_contribution_amount=Community.com_total_contribution_amount + delta,
    #             com_updated_by=user_id,
    #         )
    #     )

    #     # Direct Forane community
    #     if for_id and not par_id:
    #         await db.execute(
    #             update(Forane)
    #             .where(Forane.for_id == for_id)
    #             .values(
    #                 for_total_contribution_amount=Forane.for_total_contribution_amount + delta,
    #                 for_updated_by=user_id,
    #             )
    #         )

    #     # Community under Parish
    #     elif par_id:
    #         # Parish
    #         await db.execute(
    #             update(Parish)
    #             .where(Parish.par_id == par_id)
    #             .values(
    #                 par_total_contribution_amount=Parish.par_total_contribution_amount + delta,
    #                 par_updated_by=user_id,
    #             )
    #         )

    #         # Forane (from Parish)
    #         q2 = select(Parish.par_for_id).where(Parish.par_id == par_id)
    #         res2 = await db.execute(q2)
    #         par_for_id = res2.scalar_one_or_none()
    #         if par_for_id:
    #             await db.execute(
    #                 update(Forane)
    #                 .where(Forane.for_id == par_for_id)
    #                 .values(
    #                     for_total_contribution_amount=Forane.for_total_contribution_amount + delta,
    #                     for_updated_by=user_id,
    #                 )
    #             )

       

    
    




     
  
daoFamily:FamilyDAO = FamilyDAO(Family)





