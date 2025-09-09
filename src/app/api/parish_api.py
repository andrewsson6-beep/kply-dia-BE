from app.schema.forane_schema import ForaneInfoSchemaBase, ForaneParishRequestSchema
from app.schema.parish_schema import ParishCreateSchema
from app.service.parish_service import parishservice
from fastapi import APIRouter,Request
from common.response.response_schema import  ResponseSchemaModel, response_base
from common.security.jwt import DependsJwtAuth

router = APIRouter()

@router.post('/add-new-parish',dependencies=[DependsJwtAuth])
async def add_new_parish(obj: ParishCreateSchema) -> ResponseSchemaModel:
    data = await parishservice.add_new_parish(obj=obj)
    return response_base.success(data=data) 

@router.get('/all-parish-list',dependencies=[DependsJwtAuth])
async def parish_list_api() -> ResponseSchemaModel:
    data = await  parishservice.all_parish_list()
    return response_base.success(data=data) 

@router.post('/all_forane_parishes',dependencies=[DependsJwtAuth])
async def all_parishes_of_forane(obj: ForaneParishRequestSchema) -> ResponseSchemaModel:
    data = await  parishservice.get_parishes_by_forane(obj)
    return response_base.success(data=data) 