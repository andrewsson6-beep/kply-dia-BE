from fastapi import Request
from app.models.institution_model import Institution
from app.schema.institutions_schema import InstitutionsInfoSchemaBase
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
            
            
institutionservice: InstitutionService = InstitutionService()