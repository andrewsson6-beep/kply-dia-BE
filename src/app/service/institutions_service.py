from app.models.institution_model import Institution
from app.schema.institutions_schema import InstitutionsInfoSchemaBase
from database.db import async_db_session
from app.dao.institution_dao import dao_institutions
from common.response.response_schema import  response_base


class InstitutionService:

    """Institutions service class"""    
    @staticmethod
    async def all_institutions_list() -> Institution:
        """To List All Insitutions Who Have Paid Seperately Under The  Diocese"""
        async with async_db_session() as db:
            institutions = await  dao_institutions.institutions_list_query(db)
            if not institutions:
                return response_base.fail(data="No institutions Present")
            return [InstitutionsInfoSchemaBase.model_validate(institution) for institution in institutions]
            
            
institutionservice: InstitutionService = InstitutionService()