from app.service.individuals_service import individualservice 
from fastapi import APIRouter,Request
from common.response.response_schema import  ResponseSchemaModel, response_base
from common.security.jwt import DependsJwtAuth

router = APIRouter()


@router.get('/individuals-list',dependencies=[DependsJwtAuth])
async def individuals_list_api() -> ResponseSchemaModel:
    data = await individualservice.all_individuals_list()
    if isinstance(data, dict) and data.get("code") == 400:
        return data  
    return response_base.success(data=data) 