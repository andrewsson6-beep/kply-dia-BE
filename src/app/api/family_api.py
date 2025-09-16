from app.schema.contribution_schema import FamilContributionCreateSchema
from app.schema.family_schema import FamilyCreateSchema, FamilyRequestSchema, FamilyUpdateSchema
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
  

@router.post("/add-family-contribution", dependencies=[DependsJwtAuth])
async def create_family_contribution(request:Request,data: FamilContributionCreateSchema):
   try:
      new_family_contribution = await familyservice.family_contribution_service(request,data) 
      return response_base.success(data=new_family_contribution)
   except ValueError as e:
        return response_base.fail(data=str(e))
   except Exception as e:
        return response_base.__response(data=f"Something went wrong { str(e) }")
   


@router.post("/family-details", dependencies=[DependsJwtAuth])
async def family_details(data: FamilyRequestSchema):
   try:
      new_family_details = await familyservice.get_family_details_service(data) 
      return response_base.success(data=new_family_details)
   except ValueError as e:
        return response_base.fail(data=str(e))
   except Exception as e:
        return response_base.__response(data=f"Something went wrong { str(e) }")
   
  