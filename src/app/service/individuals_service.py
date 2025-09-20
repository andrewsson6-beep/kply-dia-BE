from fastapi import Request
from app.models.individual_model import Individual
from app.schema.individuals_schema import IndividualDetailRequestSchema, IndividualDetailSchema, IndividualUpdateSchema, IndividualsInfoSchemaBase
from common.security.jwt import get_token, jwt_decode
from database.db import async_db_session
from app.dao.individual_dao import dao_individuals
from common.response.response_schema import  response_base
from app.schema.contribution_schema import IndividualContributionCreateSchema,IndividualContributionResponseSchema, IndividualContributionUpdateSchema
from app.dao.individual_dao import dao_individuals

class IndividualsService:

    """Individuals service class"""    
    @staticmethod
    async def all_individuals_list() -> Individual:
        """To List All Individuals Who Have Paid Seperately Under The  Diocese"""
        async with async_db_session() as db:
            individuals = await dao_individuals.individuals_list_query(db)
            if not individuals:
                data="No Individuals Present"
                return data
            return [IndividualsInfoSchemaBase.model_validate(individual) for individual in individuals]
        
    @staticmethod
    async def add_new_individual(individual_data: IndividualsInfoSchemaBase):
        """Create a new Individual"""
        async with async_db_session.begin() as db:
            new_individual = await dao_individuals.create_individual(db, individual_data)
            return IndividualsInfoSchemaBase.model_validate(new_individual)


    @staticmethod   
    async def add_Individual_contribution(data: IndividualContributionCreateSchema):
        async with async_db_session.begin() as db:
            contribution = await dao_individuals.create_individuaL_contribution(db, data)
            return IndividualContributionResponseSchema.model_validate(contribution)
        
    @staticmethod 
    async def get_individual_detail(obj: IndividualDetailRequestSchema) -> IndividualDetailSchema:
        async with async_db_session() as db:
            individual = await dao_individuals.get_individual_with_contributions (db,obj)    
            if not individual:
                raise ValueError("Individual not found")
            return IndividualDetailSchema.model_validate(individual)
    
    @staticmethod 
    async def update_individual_details(request:Request, data: IndividualUpdateSchema) -> IndividualDetailSchema:
        async with async_db_session.begin() as db:
            update_data = data.model_dump(exclude_unset=True)
            individual_id = update_data.pop("ind_id")
            updated = await dao_individuals.update_individual(db, individual_id, update_data)
            if not updated:
                raise ValueError("Individual not found or already deleted")

            return IndividualDetailSchema.model_validate(updated)
    
    @staticmethod 
    async def update_contribution_details(request:Request, data:IndividualContributionUpdateSchema) -> IndividualContributionResponseSchema:
        async with async_db_session.begin() as db:
            update_data = data.model_dump(exclude_unset=True)
            contribution_id = update_data.pop("icon_id")
            updated = await dao_individuals.update_contribution(db,contribution_id, update_data)
            if not updated:
                raise ValueError("Contribution not found or already deleted")

            return IndividualContributionResponseSchema.model_validate(updated)
    

    @staticmethod 
    async def delete_individual_details(request:Request, individualId:int) -> IndividualContributionResponseSchema:
        token = get_token(request)
        user_id = jwt_decode(token).id  
        async with async_db_session.begin() as db:
            deleted = await dao_individuals.delete_individual_query(
                db, user_id=user_id, individualId=individualId
            )
            if not deleted:
                raise ValueError("Individual is  not found or already deleted")




            
            
individualservice: IndividualsService = IndividualsService()