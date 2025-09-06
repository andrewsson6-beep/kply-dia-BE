from app.schema.forane_schema import ForaneInfoSchemaBase
from app.service.forane_service import foraneservice 
from fastapi import APIRouter,Request
from common.response.response_schema import  ResponseSchemaModel, response_base
from common.security.jwt import DependsJwtAuth

router = APIRouter()


@router.get('/forane-list',dependencies=[DependsJwtAuth])
async def forane_list_api() -> ResponseSchemaModel:
    data = await  foraneservice.all_forane_list() 
    return response_base.success(data=data) 

@router.post('/add-new-forane',dependencies=[DependsJwtAuth])
async def add_new_forane(obj: ForaneInfoSchemaBase) -> ResponseSchemaModel:
    data = await  foraneservice.add_new_forane(obj) 
    return response_base.success(data=data) 