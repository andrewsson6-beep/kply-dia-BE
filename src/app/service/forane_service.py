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
            print("--------------At Service Level Before")
            foranes = await dao_forane.forane_list_query(db) 
            print("--------------At Service Level After")
            if not foranes:
                return response_base.fail(data="No Foranes Present")
            return [ForaneInfoSchemaBase.model_validate(forane) for forane in foranes]
            
            
foraneservice: ForaneService = ForaneService()