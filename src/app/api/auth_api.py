from app.schema.auth_schema import ChangePasswordSchema, LoginSchemaBase
from app.schema.user_schema import UserInfoSchemaBase
from app.service import auth_service
from fastapi import APIRouter,Request
from common.response.response_schema import  ResponseSchemaModel, response_base
from common.security.jwt import DependsJwtAuth

router = APIRouter()



@router.post('/userlogin')
async def user_login(obj: LoginSchemaBase) -> ResponseSchemaModel:
    print(obj)
    data = await auth_service.authservice.systemuser_login(obj=obj)
    if isinstance(data, dict) and data.get("code") == 400:
        return data  
    return response_base.success(data=data) 


@router.post('/changepassword',dependencies=[DependsJwtAuth])
async def change_password(request:Request,obj: ChangePasswordSchema) -> ResponseSchemaModel:
    data = await auth_service.authservice.change_password_service(obj=obj,request=request)
    if isinstance(data, dict) and data.get("code") == 400:
        return data  
    return response_base.success(data=data) 




# @router.post('/create-new-user')
# async def createNewUser(request: Request,obj: UserInfoSchemaBase) -> ResponseSchemaModel:
#     print("--------------At API CREATE USER----->")
#     print(obj.userPassword)
#     print(obj)
#     data = await auth_service.authservice.create_newuser(request=request,obj=obj)
#     if isinstance(data, dict) and data.get("code", 200) != 200:
#         return data 
#     return response_base.success(data=data)


# @router.get('/all-users')
# async def all_users(request: Request) -> ResponseSchemaModel:
#     # print("--------------At API CREATE USER----->")
#     # print(obj.userPassword)
#     # print(obj)
#     data = await auth_service.authservice.all_users_list(request=request)
#     if isinstance(data, dict) and data.get("code", 200) != 200:
#         return data 
#     return response_base.success(data=data)






