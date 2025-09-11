from app.schema.individuals_schema import IndividualDetailRequestSchema, IndividualUpdateSchema, IndividualsInfoSchemaBase
from app.schema.contribution_schema import IndividualContributionCreateSchema,IndividualContributionUpdateSchema
from app.service.individuals_service import individualservice 
from fastapi import APIRouter,Request
from common.response.response_schema import  ResponseSchemaModel, response_base
from common.security.jwt import DependsJwtAuth

router = APIRouter()

@router.get('/individuals-list',dependencies=[DependsJwtAuth])
async def individuals_list_api() -> ResponseSchemaModel:
   try:
      data = await individualservice.all_individuals_list()
      return response_base.success(data=data) 
   except ValueError as e:
        return response_base.fail(data=str(e))
   except Exception as e:
        return response_base.__response(data=f"Something went wrong { str(e) }")

@router.post("/add-new-individual", dependencies=[DependsJwtAuth])
async def add_new_individual(request: IndividualsInfoSchemaBase) -> ResponseSchemaModel:
   try:
      new_individual = await individualservice.add_new_individual(request)
      return response_base.success(data=new_individual)
   except ValueError as e:
        return response_base.fail(data=str(e))
   except Exception as e:
        return response_base.__response(data=f"Something went wrong { str(e) }")

@router.post("/add-individual-contribution", dependencies=[DependsJwtAuth])
async def create_contribution(data: IndividualContributionCreateSchema):
   try:
      new_individual_contribution = await individualservice.add_Individual_contribution(data)
      return response_base.success(data=new_individual_contribution)
   except ValueError as e:
        return response_base.fail(data=str(e))
   except Exception as e:
        return response_base.__response(data=f"Something went wrong { str(e) }")

@router.post("/individual-details", dependencies=[DependsJwtAuth])
async def create_contribution(individual_id:IndividualDetailRequestSchema):
   try:
      new_individual_contribution = await individualservice.get_individual_detail(individual_id)
      return response_base.success(data=new_individual_contribution)
   except ValueError as e:
        return response_base.fail(data=str(e))
   except Exception as e:
        return response_base.__response(data=f"Something went wrong { str(e) }")


#TO Edit the Individual Details API 
@router.put("/", dependencies=[DependsJwtAuth])
async def edit_individual(request:Request,data:IndividualUpdateSchema):
   try:
      updated_details = await individualservice.update_individual_details(request,data)
      return response_base.success(data=updated_details)
   except ValueError as e:
        return response_base.fail(data=str(e))
   except Exception as e:
        return response_base.__response(data=f"Something went wrong { str(e) }")


#TO Edit the Details Of the Specific Individual Contributions 
@router.post("/update-individual-contribution", dependencies=[DependsJwtAuth])
async def edit_contribution(request:Request,data:IndividualContributionUpdateSchema):
   try:
      updated_details=await individualservice.update_contribution_details(request,data)
      return response_base.success(data=updated_details)
   except ValueError as e:
        return response_base.fail(data=str(e))
   except Exception as e:
        return response_base.fail(data=f"Something went wrong {str(e)}")









