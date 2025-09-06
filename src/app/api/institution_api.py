from app.schema.institutions_schema import InstitutionsInfoSchemaBase
from app.service.institutions_service import InstitutionService, institutionservice
from fastapi import APIRouter, Request
from common.response.response_schema import  ResponseSchemaModel, response_base
from common.security.jwt import DependsJwtAuth

router = APIRouter()


@router.get('/institution-list',dependencies=[DependsJwtAuth])
async def institutions_list_api() -> ResponseSchemaModel:
    data = await  institutionservice.all_institutions_list()
    return response_base.success(data=data) 


@router.post("/add-new-institution", dependencies=[DependsJwtAuth])
async def add_new_institution(request:Request, obj: InstitutionsInfoSchemaBase) -> ResponseSchemaModel:
    new_institution = await institutionservice.add_new_institution(request,obj)
    return response_base.success(data=new_institution)