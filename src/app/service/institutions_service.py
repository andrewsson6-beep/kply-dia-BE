from fastapi import Request
from app.models.institution_model import Institution
from app.schema.contribution_schema import InstitutionContributionCreateSchema, InstitutionContributionResponseSchema, InstitutionContributionUpdateSchema
from app.schema.institutions_schema import InstitutionDetailRequestSchema, InstitutionDetailSchema, InstitutionUpdateSchema, InstitutionsInfoSchemaBase
from common.security.jwt import get_token, jwt_decode
from database.db import async_db_session
from app.dao.institution_dao import dao_institutions


class InstitutionService:

    """Institutions service class"""    
    @staticmethod
    async def all_institutions_list() -> Institution:
        """To List All Insitutions Who Have Paid Seperately Under The  Diocese"""
        async with async_db_session() as db:
            institutions = await  dao_institutions.institutions_list_query(db)
            if not institutions:
                data="No institutions Present"
                return data
            return [InstitutionsInfoSchemaBase.model_validate(institution) for institution in institutions]
    
    @staticmethod
    async def add_new_institution(request:Request, institution_data: InstitutionsInfoSchemaBase):
        """Create a new Institution"""
        async with async_db_session.begin() as db:
            new_institution = await dao_institutions.create_institution(db, institution_data)
            return InstitutionsInfoSchemaBase.model_validate(new_institution)
        
    @staticmethod
    async def get_institution_detail(request:Request,obj:InstitutionDetailRequestSchema) -> InstitutionDetailSchema:
        async with async_db_session() as db:
            institution = await  dao_institutions.get_institution_with_contributions(db, obj.institutionId)
            if not institution:
                raise ValueError("Institution not found")
            return InstitutionDetailSchema.model_validate(institution)
        
    
    @staticmethod   
    async def add_institution_contribution(data: InstitutionContributionCreateSchema):
        async with async_db_session.begin() as db:
            contribution = await dao_institutions.create_institution_contribution(db, data)
            return InstitutionContributionResponseSchema.model_validate(contribution)

    @staticmethod     
    async def update_institution_details(request:Request ,data: InstitutionUpdateSchema) -> InstitutionDetailSchema:
        async with async_db_session.begin() as db:
            update_data = data.model_dump(exclude_unset=True)
            ins_id = update_data.pop("ins_id")
            updated = await dao_institutions.update_institution(db, ins_id, update_data)
            if not updated:
                raise ValueError("Institution not found or already deleted")
            return InstitutionDetailSchema.model_validate(updated)
    
    @staticmethod    
    async def update_institutution_contribution_details(request:Request , data: InstitutionContributionUpdateSchema) -> InstitutionContributionResponseSchema:
        async with async_db_session.begin() as db:
            update_data = data.model_dump(exclude_unset=True)
            incon_id = update_data.pop("incon_id")
            updated = await dao_institutions.update_contribution(db, incon_id, update_data)
            if not updated:
                raise ValueError("Contribution not found or already deleted")

            return InstitutionContributionResponseSchema.model_validate(updated)
        
    @staticmethod 
    async def delete_institution_details(request:Request, institutionId:int) :
        token = get_token(request)
        user_id = jwt_decode(token).id  
        async with async_db_session.begin() as db:
            deleted = await dao_institutions.delete_institution_query(
                db, user_id=user_id, institution=institutionId
            )
            if not deleted:
                raise ValueError("Insitution is  not found or already deleted")

            
            
institutionservice: InstitutionService = InstitutionService()