from app.schema.family_schema import FamilyCreateSchema, FamilyUpdateSchema
from app.service.family_service  import familyservice
from fastapi import APIRouter,Request
from common.response.response_schema import  ResponseSchemaModel, response_base
from common.security.jwt import DependsJwtAuth

router = APIRouter()


@router.post("/create-new-family", dependencies=[DependsJwtAuth])
async def create_family_api(request:Request,data: FamilyCreateSchema) -> ResponseSchemaModel:
   try:
      new_family = await  familyservice.create_new_family(request,data) 
      return response_base.success(data=new_family)
   except ValueError as e:
        return response_base.fail(data=str(e))
   except Exception as e:
        return response_base.__response(data=f"Something went wrong { str(e) }")
   
@router.post("/update-family", dependencies=[DependsJwtAuth])
async def update_family_api(request: Request, data: FamilyUpdateSchema):
    try:
      updated_family = await  familyservice.update_family_details(request,data) 
      return response_base.success(data=updated_family)
    except ValueError as e:
        return response_base.fail(data=str(e))
    except Exception as e:
        return response_base.__response(data=f"Something went wrong { str(e) }")