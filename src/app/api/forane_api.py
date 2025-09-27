from app.schema.forane_schema import ForaneDeleteSchema, ForaneInfoSchemaBase, ForaneParishRequestSchema, ForaneUpdateSchema
from app.service.forane_service import foraneservice 
from fastapi import APIRouter,Request
from common.response.response_schema import  ResponseSchemaModel, response_base
from common.security.jwt import DependsJwtAuth

router = APIRouter()


@router.get('/forane-list',dependencies=[DependsJwtAuth])
async def forane_list_api() -> ResponseSchemaModel:
    data = await  foraneservice.all_forane_list() 
    return response_base.success(data=data) 

@router.post('/add-new-forane',dependencies=[DependsJwtAuth])
async def add_new_forane(obj: ForaneInfoSchemaBase) -> ResponseSchemaModel:
    data = await  foraneservice.add_new_forane(obj) 
    return response_base.success(data=data) 


@router.post('/forane-details',dependencies=[DependsJwtAuth])
async def forane_details(obj: ForaneParishRequestSchema) -> ResponseSchemaModel:
    data = await  foraneservice.forane__full_details(obj) 
    return response_base.success(data=data) 


@router.post("/update-forane-details", dependencies=[DependsJwtAuth])
async def edit_forane(data: ForaneUpdateSchema):
    try:
        updated_details = await foraneservice.update_forane_details_service(data)
        return response_base.success(data=updated_details)
    except ValueError as e:
        return response_base.fail(data=str(e))
    except Exception as e:
        return response_base.fail(data=f"Something went wrong {str(e)}")

@router.post("/delete-forane", dependencies=[DependsJwtAuth])
async def delete_forane(request: Request, obj: ForaneDeleteSchema) -> ResponseSchemaModel:
    try:
        msg = await foraneservice.delete_forane_service(request, obj)
        return response_base.success(data=msg)
    except ValueError as e:
        return response_base.fail(data=str(e))
    except Exception as e:
        return response_base.fail(data=f"Something went wrong: {str(e)}")



