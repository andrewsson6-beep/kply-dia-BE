from app.service.institutions_service import institutionservice
from fastapi import APIRouter
from common.response.response_schema import  ResponseSchemaModel, response_base
from common.security.jwt import DependsJwtAuth

router = APIRouter()


@router.get('/institution-list',dependencies=[DependsJwtAuth])
async def institutions_list_api() -> ResponseSchemaModel:
    data = await  institutionservice.all_institutions_list()
    if isinstance(data, dict) and data.get("code") == 400:
        return data  
    return response_base.success(data=data) 