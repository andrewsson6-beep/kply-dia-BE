
from sqlalchemy import func, insert, select
from app.models.family_model import Family
from sqlalchemy.ext.asyncio import AsyncSession

from app.schema.family_schema import FamilyCreateSchema


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
       

    
    




     
  
daoFamily:FamilyDAO = FamilyDAO(Family)





