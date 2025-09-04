from app.models.individual_model import Individual
from app.schema.individuals_schema import IndividualsInfoSchemaBase
from database.db import async_db_session
from app.dao.individual_dao import dao_individuals
from common.response.response_schema import  response_base


class IndividualsService:

    """Individuals service class"""    
    @staticmethod
    async def all_individuals_list() -> Individual:
        """To List All Individuals Who Have Paid Seperately Under The  Diocese"""
        async with async_db_session() as db:
            individuals = await dao_individuals.individuals_list_query(db)
            if not individuals:
                return response_base.fail(data="No Individuals Present")
            return [IndividualsInfoSchemaBase.model_validate(individual) for individual in individuals]
            
            
individualservice: IndividualsService = IndividualsService()