from app.schema.contribution_schema import IndividualContributionCreateSchema, InstitutionContributionCreateSchema, InstitutionContributionUpdateSchema
from app.schema.institutions_schema import InstitutionDetailRequestSchema, InstitutionUpdateSchema, InstitutionsInfoSchemaBase
from app.service.institutions_service import InstitutionService, institutionservice
from fastapi import APIRouter, Request
from common.response.response_schema import  ResponseSchemaModel, response_base
from common.response.response_code import CustomResponseCode
from common.security.jwt import DependsJwtAuth

router = APIRouter()


@router.get('/institution-list',dependencies=[DependsJwtAuth])
async def institutions_list_api() -> ResponseSchemaModel:
    try:
        data = await  institutionservice.all_institutions_list()
        return response_base.success(data=data) 
    except ValueError as e:
        return response_base.fail(data=str(e))
    except Exception as e:
        return response_base.fail(data=f"Something went wrong { str(e) }")


@router.post("/add-new-institution", dependencies=[DependsJwtAuth])
async def add_new_institution(request:Request, obj: InstitutionsInfoSchemaBase) -> ResponseSchemaModel:
    try:
        new_institution = await institutionservice.add_new_institution(request,obj)
        return response_base.success(data=new_institution)
    except ValueError as e:
        return response_base.fail(data=str(e))
    except Exception as e:
        return response_base.fail(data=f"Something went wrong { str(e) }")


@router.post("/institution-details", dependencies=[DependsJwtAuth])
async def get_institution_details(request:Request, obj: InstitutionDetailRequestSchema) -> ResponseSchemaModel:
    try:
        new_institution = await institutionservice.get_institution_detail(request, obj)
        return response_base.success(data=new_institution)
    except ValueError as e:
        return response_base.fail(data=str(e))
    except Exception as e:
        return response_base.fail(data=f"Something went wrong { str(e) }")
    

@router.post("/add-institution-contribution", dependencies=[DependsJwtAuth])
async def create_institution_contribution(data: InstitutionContributionCreateSchema):
   try:
      new_individual_contribution = await institutionservice.add_institution_contribution(data)
      return response_base.success(data=new_individual_contribution)
   except ValueError as e:
        return response_base.fail(data=str(e))
   except Exception as e:
        return response_base.fail(data=f"Something went wrong { str(e) }")






#TO Edit the Individual Details API 
@router.put("/", dependencies=[DependsJwtAuth])
async def edit_institution(request:Request,data:InstitutionUpdateSchema):
   try:
      updated_details = await institutionservice.update_institution_details(request,data)
      return response_base.success(data=updated_details)
   except ValueError as e:
        return response_base.fail(data=str(e))
   except Exception as e:
       return response_base.fail(res=CustomResponseCode.HTTP_500, data=f"Something went wrong { str(e) }")


#TO Edit the Details Of the Specific Individual Contributions 
@router.post("/update-institution-contribution", dependencies=[DependsJwtAuth])
async def edit_institution_contribution(request:Request,data:InstitutionContributionUpdateSchema):
   try:
      updated_details=await institutionservice.update_institutution_contribution_details(request,data)
      return response_base.success(data=updated_details)
   except ValueError as e:
        return response_base.fail(data=str(e))
   except Exception as e:
        return response_base.fail(data=f"Something went wrong {str(e)}")


@router.post("/delete-institution", dependencies=[DependsJwtAuth])
async def delete_institution(request: Request, data: InstitutionDetailRequestSchema):
    """Delete an Institution"""
    try:
        await institutionservice.delete_institution_details(request, data.institutionId)
        return response_base.success(data="Insstitution deleted successfully")
    except ValueError as e:
        return response_base.fail(data=str(e))
    except Exception as e:
        return response_base.fail(res=CustomResponseCode.HTTP_500, data=f"Something went wrong: {str(e)}")