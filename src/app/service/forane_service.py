from fastapi import Request
from app.dao import forane_dao
from app.models.forane_model import Forane
from app.schema.forane_schema import ForaneInfoSchemaBase
from database.db import async_db_session
from app.dao.forane_dao import dao_forane
from common.response.response_schema import  response_base


class ForaneService:
    """Forane service class"""    
    @staticmethod
    async def all_forane_list() -> Forane:
        """To List All Forane Under The  Diocese"""
        async with async_db_session() as db:
            foranes = await dao_forane.forane_list_query(db)
            if not foranes:  
                data="No Foranes Present"
                return data
            return [ForaneInfoSchemaBase.model_validate(forane) for forane in foranes]
        
    @staticmethod
    async def add_new_forane(forane_data: ForaneInfoSchemaBase):
        """To Add A New Forane In The Diocese"""
        async with async_db_session() as db:
            new_forane = await dao_forane.create_forane(db, forane_data)
            return ForaneInfoSchemaBase.model_validate(new_forane)
        
    
   
        
            
            
foraneservice: ForaneService = ForaneService()