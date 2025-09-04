from app.models.systemuser_model import SystemUser
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from sqlalchemy.orm import selectinload


class CRUDUser:
    """User database operation class"""

    def __init__(self, model):
        self.model = model


    async def getuser_by_email(self, db: AsyncSession, email: str):
        stmt = (
            select(self.model).options(
                selectinload(self.model.role)
            ).where(self.model.usr_email == email)
        )
        result = await db.execute(stmt)
        return result.scalar()
    
   
    # async def create_user(self, db: AsyncSession, obj_data: dict) -> SystemUser:
    #     """
    #     Insert a new user into the database.
    #     """
    #     stmt = insert(self.model).values(**obj_data).returning(self.model)
    #     result = await db.execute(stmt)
    #     await db.commit()
    #     return result.scalar_one()
    
    
    # async def all_users_query(self, db: AsyncSession) -> SystemUser:

    #    stmt = (select(self.model))
    #    result = await db.execute(stmt)
    #    return result.scalars()
    

    """Get The User Details By User Id"""
    async def get_user_details_by_id(self, db: AsyncSession, user_id: str):
        stmt = (
            select(self.model).options(
                selectinload(self.model.role)
            ).where(self.model.usr_id == user_id)
        )
        result = await db.execute(stmt)
        return result.scalar()
    
    "Update The Password Of The User"
    async def update_user_password(self, db: AsyncSession,user_id:int , new_hashed_password: str):
        print('At Query Page------------->',new_hashed_password)
        print('user_id',user_id)
        stmt = (
            update(self.model).where(self.model.usr_id == user_id).values(
                usr_password_hash=new_hashed_password
            )
        )
        print(stmt)
        result = await db.execute(stmt)
        await db.commit()                   

        return result.rowcount or 0


        
  
user_dao:CRUDUser = CRUDUser(SystemUser)





