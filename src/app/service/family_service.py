from fastapi import Request
from app.models.family_model import Family
from app.schema.contribution_schema import FamilContributionResponseSchema
from common.security.jwt import get_token, jwt_decode
from database.db import async_db_session
from app.dao.family_dao import daoFamily
from app.schema.family_schema  import FamilyCreateSchema, FamilyDetailsResponseSchema, FamilyRequestSchema,FamilyResponseSchema,FamilyUpdateSchema


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
        
    @staticmethod
    async def update_family_details(request:Request,data:FamilyUpdateSchema) -> Family:
        """To Update the details of the Family Under the Community"""
        token = get_token(request)
        user_id = jwt_decode(token).id  
        async with async_db_session.begin() as db:
            update_data = data.model_dump(exclude_unset=True)
            family_id = update_data.pop("fam_id")

            update_data["fam_updated_by"] = user_id  

            updated = await daoFamily.update_family(db, family_id, update_data)
            if not updated:
                raise ValueError("Family not found or already deleted")

            return FamilyResponseSchema.model_validate(updated)
        
    @staticmethod
    async def family_contribution_service(request:Request,data:FamilyUpdateSchema) -> Family:
        """To Add the Family Contribution Detail"""
        token = get_token(request)
        user_id = jwt_decode(token).id  
        async with async_db_session.begin() as db:
            contribution = await daoFamily.create_family_contribution(db, user_id=user_id,data=data)
            return FamilContributionResponseSchema.model_validate(contribution)
        

    @staticmethod
    async def get_family_details_service(data:FamilyRequestSchema) -> Family:
        """To Get the Family Details"""
        async with async_db_session() as db:
            contribution = await daoFamily.get_family_with_contributions(db,fam_id=data.fam_id)
            if not contribution:
                raise ValueError("Family not found")
            return  FamilyDetailsResponseSchema.model_validate(contribution)
        
    @staticmethod
    async def update_family_contribution_service(request, data):
        """Service to update a family contribution"""
        token = get_token(request)
        user_id = jwt_decode(token).id  

        async with async_db_session.begin() as db:
            contribution = await daoFamily.update_family_contribution(
                db, user_id=user_id, data=data
            )
            return FamilContributionResponseSchema.model_validate(contribution)

    @staticmethod
    async def delete_family_contribution_service(request, data):
        """Service to delete a family contribution"""
        token = get_token(request)
        user_id = jwt_decode(token).id  

        async with async_db_session.begin() as db:
            deleted = await daoFamily.delete_family_contribution(
                db, user_id=user_id, fcon_id=data
            )
            if not deleted:
                raise ValueError("Contribution not found or already deleted")
        
    
    



       
    

   
    
   
        
    
   
        
            
            
familyservice: FamilyService = FamilyService()