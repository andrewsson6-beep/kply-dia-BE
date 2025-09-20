from fastapi import Request

from app.models.parish_model import Parish
from app.schema.forane_schema import ForaneParishRequestSchema
from app.schema.parish_schema import ParishCreateSchema, ParishDetailSchema, ParishResponseSchema, ParishUpdateSchema
from common.security.jwt import get_token, jwt_decode
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
    


    @staticmethod
    async def get_parish_details_service(requst:Request,par_id: int) -> ParishDetailSchema:
        async with async_db_session() as db:
            parish = await dao_parishs.get_parish_details(db, par_id)
            if not parish:
                raise ValueError("Parish not found or deleted")
            return ParishDetailSchema.model_validate(parish)

    @staticmethod
    async def update_parish_details_service(request: Request, data: ParishUpdateSchema) -> ParishDetailSchema:
        token = get_token(request)
        user_id = jwt_decode(token).id

        async with async_db_session.begin() as db:
            update_data = data.model_dump(exclude_unset=True)
            par_id = update_data.pop("par_id")

            updated = await dao_parishs.update_parish_details(db, par_id, update_data, user_id)
            if not updated:
                raise ValueError("Parish not found or already deleted")

            return ParishDetailSchema.model_validate(updated)
        
            
            
parishservice: ParishService = ParishService()