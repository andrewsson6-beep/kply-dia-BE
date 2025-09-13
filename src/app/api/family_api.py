from app.schema.family_schema import FamilyCreateSchema
from app.service.family_service  import familyservice
from fastapi import APIRouter,Request
from common.response.response_schema import  ResponseSchemaModel, response_base
from common.security.jwt import DependsJwtAuth

router = APIRouter()


@router.post("/create-new-family", dependencies=[DependsJwtAuth])
async def create_family_api(request:Request,data: FamilyCreateSchema) -> ResponseSchemaModel:
   try:
      new_community = await  familyservice.create_new_family(request,data) 
      return response_base.success(data=new_community)
   except ValueError as e:
        return response_base.fail(data=str(e))
   except Exception as e:
        return response_base.__response(data=f"Something went wrong { str(e) }")