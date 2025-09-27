from fastapi import Request
from app.models.community_model import Community
from app.models.forane_model import Forane
from app.schema.community_schema import CommunityCreateSchema, CommunityDeleteSchema, CommunityDetailSchema, CommunityListRequestSchema, CommunityRequestSchema, CommunityResponseSchema, CommunityUpdateSchema
from app.schema.forane_schema import ForaneInfoSchemaBase
from common.security.jwt import get_token, jwt_decode
from database.db import async_db_session
from app.dao.community_dao import daoCommunity


class CommunityService:
    """Community service class"""   

    @staticmethod
    async def create_community_service(request:Request,data:CommunityCreateSchema) -> Community:
        """To Create A Community Under the Parish Or Diocese"""
        token = get_token(request)
        user_id = jwt_decode(token).id  
        async with async_db_session.begin() as db:
            result = await  daoCommunity.create_community(db=db,user_id=user_id,community_data=data)
            if not result:
                raise ValueError("Community Cannot Be Created")
            return CommunityResponseSchema.model_validate(result)
    

    @staticmethod
    async def community_list_service(request:Request,data:CommunityListRequestSchema) -> Community:
        """To Create A Community Under the Parish Or Diocese"""
        token = get_token(request)
        user_id = jwt_decode(token).id  
        async with async_db_session() as db:
            communities = await  daoCommunity.get_communities(db=db,user_id=user_id,data=data)
            if not communities:
                raise ValueError("No Communities Present")
            return [CommunityResponseSchema.model_validate(c) for c in communities]
    

    
    @staticmethod
    async def community_details_service(request:Request,data:CommunityRequestSchema) -> CommunityDetailSchema:
        """To List the details of the commiunty include the family details"""
        token = get_token(request)
        user_id = jwt_decode(token).id  
        async with async_db_session() as db:
            community = await  daoCommunity.get_community_detail(db=db,community_id=data.com_id)
            if not community:
                raise ValueError("Community not found")
            return CommunityDetailSchema.model_validate(community)
    

    @staticmethod
    async def update_community_details(request: Request, data: CommunityUpdateSchema) -> CommunityDetailSchema:
        token = get_token(request)
        user_id = jwt_decode(token).id  
        async with async_db_session.begin() as db:
            update_data = data.model_dump(exclude_unset=True)
            community_id = update_data.pop("com_id")
            update_data["com_updated_by"] = user_id

            updated = await daoCommunity.update_community(db,community_id, update_data)
            if not updated:
                raise ValueError("Community not found or already deleted")

            return CommunityDetailSchema.model_validate(updated)
        
    
    @staticmethod
    async def delete_community_service(request: Request, data: CommunityDeleteSchema) -> str:
        token = get_token(request)
        user_id = jwt_decode(token).id

        async with async_db_session.begin() as db:
            deleted = await daoCommunity.delete_community(db, data.com_id, user_id)
            if not deleted:
                raise ValueError("Community not found or already deleted")
            return f"Community with ID {data.com_id} deleted successfully"
        
    
    
   
        
    
   
        
            
            
communityservice: CommunityService = CommunityService()