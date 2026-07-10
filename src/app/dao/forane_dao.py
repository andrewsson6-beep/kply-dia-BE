from app.models.forane_model import Forane
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, insert, select, update
from sqlalchemy.orm import selectinload,noload
from app.models.community_model import Community
from app.models.family_model import Family
from app.models.familycontribution_model import FamilyContribution
from app.models.parish_model import Parish
from app.models.systemuser_model import SystemUser
from app.schema.forane_schema import ForaneInfoSchemaBase


class ForaneDAO:
    """Forane database operation class"""

    def __init__(self, model):
        self.model = model
    
    async def forane_list_query(self, db: AsyncSession) -> list[Forane]:
        stmt = (
            select(self.model)
            .where(self.model.for_is_deleted == False)  # Exclude deleted foranes
        )
        result = await db.execute(stmt)
        foranes = result.scalars().all()
        await self._apply_forane_totals(db, foranes)
        return foranes


    async def create_forane(self, db: AsyncSession, forane_data: ForaneInfoSchemaBase) -> Forane:

        # Generate next unique number
        stmt_max = select(func.max(self.model.for_id))
        result = await db.execute(stmt_max)
        max_unique_no = result.scalar() or 0
        new_unique_no = max_unique_no + 1

        # Generate institution code from unique number
        new_code = f"FORANE-{new_unique_no:04d}"   # e.g., INS-0001

        stmt = (
            insert(self.model)
            .values(
                for_code=new_code,
                for_unique_no=new_unique_no,
                for_name=forane_data.forName,
                for_location=forane_data.forLocation,
                for_vicar_name=forane_data.forVicarName,
                # for_total_contribution_amount=forane_data.forTotalContribution,
                for_contact_number=forane_data.forContactNumber,
            )
            .returning(self.model)   # so we get the inserted row back
        )
        result = await db.execute(stmt)
        await db.commit()
        return result.scalar_one()
    

    async def get_forane_with_parishes(self, db: AsyncSession, forane_id: int) -> Forane | None:
        stmt = (
            select(self.model)
            .options(selectinload(self.model.parishes),selectinload(self.model.communities))  # eager load parishes
            .where(self.model.for_id == forane_id, self.model.for_is_deleted == False)
        )
        result = await db.execute(stmt)
        forane = result.scalar_one_or_none()
        if forane:
            await self._apply_forane_totals(db, [forane])
            await self._apply_parish_totals(db, forane.parishes)
            await self._apply_community_totals(db, forane.communities)
        return forane

    async def _apply_forane_totals(self, db: AsyncSession, foranes: list[Forane]) -> None:
        forane_ids = [forane.for_id for forane in foranes]
        if not forane_ids:
            return

        stmt = (
            select(
                func.coalesce(Community.com_for_id, Parish.par_for_id).label("forane_id"),
                func.coalesce(func.sum(FamilyContribution.fcon_amount), 0),
            )
            .select_from(Community)
            .outerjoin(Parish, Parish.par_id == Community.com_par_id)
            .join(Family, Family.fam_com_id == Community.com_id)
            .join(FamilyContribution, FamilyContribution.fcon_fam_id == Family.fam_id)
            .where(
                func.coalesce(Community.com_for_id, Parish.par_for_id).in_(forane_ids),
                Community.com_is_deleted == False,
                Family.fam_is_deleted == False,
                FamilyContribution.fcon_is_deleted == False,
            )
            .group_by(func.coalesce(Community.com_for_id, Parish.par_for_id))
        )
        result = await db.execute(stmt)
        totals = dict(result.all())
        for forane in foranes:
            forane.for_total_contribution_amount = totals.get(forane.for_id, 0)

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
    
    async def update_forane_details(self, db: AsyncSession, forane_id: int, update_data: dict) -> Forane | None:
        stmt = (
            update(self.model)
            .where(self.model.for_id == forane_id, self.model.for_is_deleted == False)
            .values(**update_data)
            .returning(self.model).options(noload(Forane.parishes))
        )
        result = await db.execute(stmt)
        await db.commit()
        forane = result.scalar_one_or_none()
        if forane:
            await self._apply_forane_totals(db, [forane])
        return forane
    
    async def delete_forane(self, db: AsyncSession, for_id: int, user_id: int) -> Forane | None:
        stmt = (
            update(self.model)
            .where(self.model.for_id == for_id, self.model.for_is_deleted == False)
            .values(for_is_deleted=True, for_updated_by=user_id)
            .returning(self.model)
        )
        result = await db.execute(stmt)
        return result.scalar_one_or_none()
    

    

dao_forane:ForaneDAO = ForaneDAO(Forane)





