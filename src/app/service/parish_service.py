from fastapi import Request

from app.models.parish_model import Parish
from app.schema.forane_schema import ForaneParishRequestSchema
from app.schema.parish_schema import ParishCreateSchema, ParishResponseSchema
from database.db import async_db_session
from common.response.response_schema import  response_base
from app.dao.parish_dao import dao_parishs


class ParishService:
    """Parish service class"""    
   
        
    @staticmethod
    async def add_new_parish(obj: ParishCreateSchema):
        """To Add A New Parish To The Forane"""
        async with async_db_session.begin() as db:
            new_parish = await dao_parishs.create_parish(db,obj)
            return ParishResponseSchema.model_validate(new_parish)
        
    @staticmethod
    async def all_parish_list() -> Parish:
        """To List All Parishes Under The  Diocese"""
        async with async_db_session() as db:
            parishes = await  dao_parishs.parish_list_query(db=db)
            if not parishes:  
                data="No Parishes Present"
                return data
            return [ParishResponseSchema.model_validate(parish) for parish in parishes]
        
    
    @staticmethod
    async def get_parishes_by_forane(obj:ForaneParishRequestSchema) -> Parish:
        """To List All Parishes Under The  Forane"""
        async with async_db_session() as db:
            parishes = await  dao_parishs.get_parishes_by_forane(db=db,forane_id=obj.foraneId)
            if not parishes:  
                data="No Parishes Present For This Forane"
                return data
            return [ParishResponseSchema.model_validate(parish) for parish in parishes]
        
            
            
parishservice: ParishService = ParishService()