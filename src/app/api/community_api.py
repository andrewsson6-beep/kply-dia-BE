from app.schema.community_schema import CommunityCreateSchema, CommunityDeleteSchema, CommunityListRequestSchema, CommunityRequestSchema, CommunityUpdateSchema
from app.service.community_service import communityservice 
from fastapi import APIRouter,Request
from common.response.response_schema import  ResponseSchemaModel, response_base
from common.security.jwt import DependsJwtAuth

router = APIRouter()


@router.post("/create-new-community", dependencies=[DependsJwtAuth])
async def create_community_api(request:Request,data: CommunityCreateSchema) -> ResponseSchemaModel:
   try:
      new_community = await  communityservice.create_community_service(request,data)
      return response_base.success(data=new_community)
   except ValueError as e:
        return response_base.fail(data=str(e))
   except Exception as e:
        return response_base.__response(data=f"Something went wrong { str(e) }")


@router.post("/community-list", dependencies=[DependsJwtAuth])
async def list_communities(request:Request,data: CommunityListRequestSchema):
    try:
      community_list = await  communityservice.community_list_service(request,data)
      return response_base.success(data=community_list)
    except ValueError as e:
        return response_base.fail(data=str(e))
    except Exception as e:
        return response_base.__response(data=f"Something went wrong { str(e) }")


@router.post("/community-details", dependencies=[DependsJwtAuth])
async def community_details(request:Request,data: CommunityRequestSchema):
    try:
      community_list = await  communityservice.community_details_service(request,data)
      return response_base.success(data=community_list)
    except ValueError as e:
        return response_base.fail(data=str(e))
    except Exception as e:
        return response_base.__response(data=f"Something went wrong { str(e) }")


@router.post("/update-community",dependencies=[DependsJwtAuth])
async def edit_community(data: CommunityUpdateSchema, request: Request):
    try:
        updated_details = await communityservice.update_community_details(request, data)
        return response_base.success(data=updated_details)
    except ValueError as e:
        return response_base.fail(data=str(e))
    except Exception as e:
        return response_base.__response(data=f"Something went wrong { str(e) }")


@router.post("/delete-community", dependencies=[DependsJwtAuth])
async def delete_community(request: Request, obj: CommunityDeleteSchema) -> ResponseSchemaModel:
    try:
        msg = await communityservice.delete_community_service(request, obj)
        return response_base.success(data=msg)
    except ValueError as e:
        return response_base.fail(data=str(e))
    except Exception as e:
        return response_base.fail(data=f"Something went wrong: {str(e)}")
 
  


