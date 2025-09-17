
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, insert, select, update
from sqlalchemy.orm import selectinload
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
                par_is_deleted=False
            )
            .returning(self.model)  # return the inserted row
        )

        result = await db.execute(stmt)
        await db.commit()
        return result.scalar_one()
    

    async def parish_list_query(self, db: AsyncSession) -> Parish:
       stmt = (select(self.model).where(self.model.par_is_deleted==False))
       result = await db.execute(stmt)
       return result.scalars().all()
    
    async def get_parishes_by_forane(self, db: AsyncSession, forane_id: int) -> list[Parish]:
        stmt = select(self.model).where(
            self.model.par_for_id == forane_id,
            self.model.par_is_deleted == False
        )
        result = await db.execute(stmt)
        return result.scalars().all()
    


    async def get_parish_details(self, db: AsyncSession, par_id: int) -> Parish | None:
        stmt = (
            select(self.model)
            .options(selectinload(self.model.communities))
            .where(self.model.par_id == par_id, self.model.par_is_deleted == False)
        )
        result = await db.execute(stmt)
        return result.scalar_one_or_none()

    async def update_parish_details(self, db: AsyncSession, par_id: int, update_data: dict, user_id: int) -> Parish | None:
        stmt = (
            update(self.model)
            .where(self.model.par_id == par_id, self.model.par_is_deleted == False)
            .values(**update_data, par_updated_by=user_id)
            .returning(self.model)
        )
        result = await db.execute(stmt)
        return result.scalar_one_or_none()
    

    

dao_parishs:ParishDAO = ParishDAO(Parish)





