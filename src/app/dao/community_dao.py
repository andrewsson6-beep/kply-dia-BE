from typing import List
from app.models.community_model import Community
from app.models.family_model import Family
from app.models.systemuser_model import SystemUser
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, insert, select, update
from sqlalchemy.orm import selectinload,noload

from app.schema.community_schema import CommunityCreateSchema, CommunityDetailSchema, CommunityListRequestSchema, CommunityResponseSchema, CommunityUpdateSchema


class CommunityDAO:
    """Community Dao Class Operation"""

    def __init__(self, model):
        self.model = model
    
    async def create_community(self, db: AsyncSession,user_id:int,community_data:CommunityCreateSchema ) -> Community:
        """"""
        # Generate unique number
        stmt_max = select(func.max(self.model.com_unique_no))
        result = await db.execute(stmt_max)
        max_unique_no = result.scalar() or 0
        new_unique_no = max_unique_no + 1

        # Generate code
        new_code = f"COM-{new_unique_no:04d}"

        stmt = (
            insert(self.model)
            .values(
                com_for_id=community_data.com_for_id,
                com_par_id=community_data.com_par_id,
                com_name=community_data.com_name,
                com_created_by=user_id,
                com_unique_no=new_unique_no,
                com_code=new_code,
            )
            .returning(self.model)
        )
        result = await db.execute(stmt)
        await db.commit()
        return result.scalar_one()
       

    
    async def get_communities(self, db: AsyncSession,user_id:int, data:CommunityListRequestSchema) -> List[CommunityResponseSchema]:
        query = select(self.model).where(self.model.com_is_deleted == False)

        if data.forane_id:
            query = query.where(self.model.com_for_id == data.forane_id)
        if data.parish_id:
            query = query.where(self.model.com_par_id == data.parish_id)

        result = await db.execute(query)
        communities = result.scalars().all()
        return communities
    
    async def get_community_detail(self, db: AsyncSession, community_id: int) :
        stmt = (
            select(self.model).options(selectinload(Community.families))
            .where(self.model.com_id == community_id, self.model.com_is_deleted == False)
        )
        result = await db.execute(stmt)
        community = result.scalar_one_or_none()
        return community
    

    async def update_community(self, db: AsyncSession, community_id: int, update_data: dict) -> Community | None:
        stmt = (
            update(self.model)
            .where(self.model.com_id == community_id, self.model.com_is_deleted == False)
            .values(**update_data)
            .returning(self.model).options(noload(Community.families))
        )
        result = await db.execute(stmt)
        await db.commit()
        return result.scalar_one_or_none()
    
    async def delete_community(self, db: AsyncSession, com_id: int, user_id: int) -> Community | None:
        stmt = (
            update(self.model)
            .where(self.model.com_id == com_id, self.model.com_is_deleted == False)
            .values(com_is_deleted=True, com_updated_by=user_id)
            .returning(self.model)
        )
        result = await db.execute(stmt)
        return result.scalar_one_or_none()




     
  
daoCommunity:CommunityDAO = CommunityDAO(Community)





