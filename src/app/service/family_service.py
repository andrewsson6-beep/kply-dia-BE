from fastapi import Request
from app.models.family_model import Family
from common.security.jwt import get_token, jwt_decode
from database.db import async_db_session
from app.dao.family_dao import daoFamily
from app.schema.family_schema  import FamilyCreateSchema,FamilyResponseSchema


class FamilyService:
    """Family service class"""   

    @staticmethod
    async def create_new_family(request:Request,data:FamilyCreateSchema) -> Family:
        """To Create A Family Under the Community"""
        token = get_token(request)
        user_id = jwt_decode(token).id  
        async with async_db_session.begin() as db:
            result = await  daoFamily.create_family(db=db,user_id=user_id,family_data=data) 
            if not result:
                raise ValueError("Family Cannot Be Created")
            return FamilyResponseSchema.model_validate(result)
       
    

   
    
   
        
    
   
        
            
            
familyservice: FamilyService = FamilyService()