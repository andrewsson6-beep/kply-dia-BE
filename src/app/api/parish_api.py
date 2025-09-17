from app.schema.forane_schema import ForaneInfoSchemaBase, ForaneParishRequestSchema
from app.schema.parish_schema import ParishCreateSchema, ParishRequestSchema, ParishUpdateSchema
from app.service.parish_service import parishservice
from fastapi import APIRouter,Request
from common.response.response_schema import  ResponseSchemaModel, response_base
from common.security.jwt import DependsJwtAuth

router = APIRouter()

@router.post('/add-new-parish',dependencies=[DependsJwtAuth])
async def add_new_parish(obj: ParishCreateSchema) -> ResponseSchemaModel:
    data = await parishservice.add_new_parish(obj=obj)
    return response_base.success(data=data) 

@router.get('/all-parish-list',dependencies=[DependsJwtAuth])
async def parish_list_api() -> ResponseSchemaModel:
    data = await  parishservice.all_parish_list()
    return response_base.success(data=data) 

@router.post('/all_forane_parishes',dependencies=[DependsJwtAuth])
async def all_parishes_of_forane(obj: ForaneParishRequestSchema) -> ResponseSchemaModel:
    data = await  parishservice.get_parishes_by_forane(obj)
    return response_base.success(data=data) 



@router.post("/update-parish-details", dependencies=[DependsJwtAuth])
async def edit_parish_details(request:Request, data: ParishUpdateSchema):
    try:
        updated_details = await parishservice.update_parish_details_service(request,data)
        return response_base.success(data=updated_details)
    except ValueError as e:
        return response_base.fail(data=str(e))
    except Exception as e:
        return response_base.fail(data=f"Something went wrong {str(e)}")
    
@router.post("/parish-details", dependencies=[DependsJwtAuth])
async def parish_details(request:Request, data: ParishRequestSchema):
    try:
        parish_details = await parishservice.get_parish_details_service(request,data.par_id)
        return response_base.success(data=parish_details)
    except ValueError as e:
        return response_base.fail(data=str(e))
    except Exception as e:
        return response_base.fail(data=f"Something went wrong {str(e)}")
