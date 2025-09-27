from app.models.forane_model import Forane
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, insert, select, update
from sqlalchemy.orm import selectinload,noload
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
        return result.scalars().all()


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
        return result.scalar_one_or_none()
    
    async def update_forane_details(self, db: AsyncSession, forane_id: int, update_data: dict) -> Forane | None:
        stmt = (
            update(self.model)
            .where(self.model.for_id == forane_id, self.model.for_is_deleted == False)
            .values(**update_data)
            .returning(self.model).options(noload(Forane.parishes))
        )
        result = await db.execute(stmt)
        await db.commit()
        return result.scalar_one_or_none()
    
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





