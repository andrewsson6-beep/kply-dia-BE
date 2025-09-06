from app.schema.individuals_schema import IndividualsInfoSchemaBase
from app.service.individuals_service import individualservice 
from fastapi import APIRouter,Request
from common.response.response_schema import  ResponseSchemaModel, response_base
from common.security.jwt import DependsJwtAuth

router = APIRouter()


@router.get('/individuals-list',dependencies=[DependsJwtAuth])
async def individuals_list_api() -> ResponseSchemaModel:
    data = await individualservice.all_individuals_list()
    return response_base.success(data=data) 


@router.post("/add-new-individual", dependencies=[DependsJwtAuth])
async def add_new_individual(request: IndividualsInfoSchemaBase) -> ResponseSchemaModel:
    new_individual = await individualservice.add_new_individual(request)
    return response_base.success(data=new_individual)