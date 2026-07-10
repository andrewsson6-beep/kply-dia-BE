
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, insert, select, update
from sqlalchemy.orm import selectinload,noload
from app.models.community_model import Community
from app.models.family_model import Family
from app.models.familycontribution_model import FamilyContribution
from app.models.parish_model import Parish
from app.models.systemuser_model import SystemUser
from app.schema.parish_schema import ParishCreateSchema



class ParishDAO:
    """Parish database operation class"""

    def __init__(self, model):
        self.model = model
    
    async def create_parish(self, db: AsyncSession, parish_data: ParishCreateSchema) -> Parish:
        # Generate next unique number
        stmt_max = select(func.max(self.model.par_unique_no))
        result = await db.execute(stmt_max)
        max_unique_no = result.scalar() or 0
        new_unique_no = max_unique_no + 1

        # Generate Parish code
        new_code = f"PAR-{new_unique_no:04d}"  # e.g., PAR-0001

        # Insert into DB
        stmt = (
            insert(self.model)
            .values(
                par_for_id=parish_data.parForId,
                par_unique_no=new_unique_no,
                par_code=new_code,
                par_name=parish_data.parName,
                par_location=parish_data.parLocation,
                par_vicar_name=parish_data.parVicarName,
                par_total_contribution_amount=parish_data.parTotalContribution or 0,
                par_is_deleted=False,
                par_contact_number=parish_data.parContactNumber
            )
            .returning(self.model)  # return the inserted row
        )

        result = await db.execute(stmt)
        await db.commit()
        return result.scalar_one()
    

    async def parish_list_query(self, db: AsyncSession) -> list[Parish]:
        stmt = (
            select(self.model)
            .where(self.model.par_is_deleted == False)  # exclude deleted
        )
        result = await db.execute(stmt)
        parishes = result.scalars().all()
        await self._apply_parish_totals(db, parishes)
        return parishes

    
    async def get_parishes_by_forane(self, db: AsyncSession, forane_id: int) -> list[Parish]:
        stmt = select(self.model).where(
            self.model.par_for_id == forane_id,
            self.model.par_is_deleted == False
        )
        result = await db.execute(stmt)
        parishes = result.scalars().all()
        await self._apply_parish_totals(db, parishes)
        return parishes
    


    async def get_parish_details(self, db: AsyncSession, par_id: int) -> Parish | None:
        stmt = (
            select(self.model)
            .options(selectinload(self.model.communities))
            .where(self.model.par_id == par_id, self.model.par_is_deleted == False)
        )
        result = await db.execute(stmt)
        parish = result.scalar_one_or_none()
        if parish:
            await self._apply_parish_totals(db, [parish])
            await self._apply_community_totals(db, parish.communities)
        return parish

    async def _apply_parish_totals(self, db: AsyncSession, parishes: list[Parish]) -> None:
        parish_ids = [parish.par_id for parish in parishes]
        if not parish_ids:
            return

        stmt = (
            select(
                Community.com_par_id,
                func.coalesce(func.sum(FamilyContribution.fcon_amount), 0),
            )
            .join(Family, Family.fam_com_id == Community.com_id)
            .join(FamilyContribution, FamilyContribution.fcon_fam_id == Family.fam_id)
            .where(
                Community.com_par_id.in_(parish_ids),
                Community.com_is_deleted == False,
                Family.fam_is_deleted == False,
                FamilyContribution.fcon_is_deleted == False,
            )
            .group_by(Community.com_par_id)
        )
        result = await db.execute(stmt)
        totals = dict(result.all())
        for parish in parishes:
            parish.par_total_contribution_amount = totals.get(parish.par_id, 0)

    async def _apply_community_totals(self, db: AsyncSession, communities: list[Community]) -> None:
        community_ids = [community.com_id for community in communities]
        if not community_ids:
            return

        stmt = (
            select(
                Family.fam_com_id,
                func.coalesce(func.sum(FamilyContribution.fcon_amount), 0),
            )
            .join(FamilyContribution, FamilyContribution.fcon_fam_id == Family.fam_id)
            .where(
                Family.fam_com_id.in_(community_ids),
                Family.fam_is_deleted == False,
                FamilyContribution.fcon_is_deleted == False,
            )
            .group_by(Family.fam_com_id)
        )
        result = await db.execute(stmt)
        totals = dict(result.all())
        for community in communities:
            community.com_total_contribution_amount = totals.get(community.com_id, 0)

    async def update_parish_details(self, db: AsyncSession, par_id: int, update_data: dict, user_id: int) -> Parish | None:
        stmt = (
            update(self.model)
            .where(self.model.par_id == par_id, self.model.par_is_deleted == False)
            .values(**update_data, par_updated_by=user_id)
            .returning(self.model).options(noload(self.model.communities)) 
        )
        result = await db.execute(stmt)
        parish = result.scalar_one_or_none()
        if parish:
            await self._apply_parish_totals(db, [parish])
        return parish

    async def delete_parish(self, db: AsyncSession, par_id: int, user_id: int) -> Parish | None:
        stmt = (
            update(self.model)
            .where(self.model.par_id == par_id, self.model.par_is_deleted == False)
            .values(par_is_deleted=True, par_updated_by=user_id)
            .returning(self.model)
        )
        result = await db.execute(stmt)
        return result.scalar_one_or_none()
    
    

    

dao_parishs:ParishDAO = ParishDAO(Parish)





