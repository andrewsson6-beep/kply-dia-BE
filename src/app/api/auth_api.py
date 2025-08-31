from fastapi import APIRouter
from common.response.response_schema import  ResponseSchemaModel, response_base

router = APIRouter()
@router.get('/userlogin')
async def user_login() -> ResponseSchemaModel:
 
    return response_base.success(data="Hello") 