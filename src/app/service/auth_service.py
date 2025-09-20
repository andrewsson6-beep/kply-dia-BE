from email import errors
from app.models.systemuser_model import SystemUser
from app.schema.auth_schema import ChangePasswordSchema, LoginSchemaBase, UserAuthenticatedDetails
from app.schema.user_schema import UserCreateSchema, UserInfoSchemaBase
from common.security.jwt import create_access_token, get_token, jwt_decode, password_verify
from database.db import async_db_session
from common.response.response_schema import  response_base
from app.dao.user_dao import user_dao
from fastapi import Request
import bcrypt
from common.security.jwt import get_hash_password

class AuthService:
    """Auth service class"""
    @staticmethod
    async def user_verify(*, obj: LoginSchemaBase):
        try:
            async with async_db_session() as db:
                user = await user_dao.getuser_by_email(db, obj.useremail)
                print(user)
                if not user:
                    raise errors.NotFoundError(msg="Not Found Error")
                if user.usr_password_hash is None:
                    return response_base.fail(data="Autorisation Error")
                else:
                    if not password_verify(obj.userpassword, user.usr_password_hash):
                        return response_base.fail(data="Autorisation Error")
                return response_base.success(data=user)

        except Exception as e:
            print("AT Exception ", e)
            return response_base.fail(data=f"Something went wrong and error {e}")
    

    async def systemuser_login(self, *, obj: LoginSchemaBase):
        async with async_db_session.begin() as db:
            system_user = None
            system_user = await self.user_verify(obj=obj)
            if system_user.code == 400:
                return {
                    "code": 400,
                    "msg": "Bad Request",
                    "status": "Success",
                    "data": "Invalid Credentials",
                }
            if system_user.code == 200:
                a_token = await create_access_token(
                    user_id=str(system_user.data.usr_id),
                )
                data = UserAuthenticatedDetails(
                    userId=system_user.data.usr_id,
                    access_token=a_token.access_token,
                    access_token_expire_time=a_token.access_token_expire_time,
                    session_uuid=a_token.session_uuid,
                    userEmail=system_user.data.usr_email,
                    userfirstName=system_user.data.usr_full_name,
                    userRoleId=system_user.data.usr_rol_id,
                    userName=system_user.data.usr_username,
                )
                return data
    





    
    async def create_newuser(self, request, obj: UserCreateSchema) -> UserInfoSchemaBase | dict:
        async with async_db_session.begin() as db:
            # Check duplicate email
            existing_user = await user_dao.getuser_by_email(db, obj.userEmail)
            if existing_user:
                return {
                    "code": 400,
                    "msg": "User already exists",
                    "data": obj.userEmail
                }

            # Hash password
            salt = bcrypt.gensalt()
            hashed_pw = get_hash_password(obj.userPassword,salt)

            # Prepare data for DB
            user_dict = {
                "usr_username": obj.userName,
                "usr_email": obj.userEmail,
                "usr_password_hash": hashed_pw,
                "usr_rol_id": obj.userRoleId,
                "usr_status": "active"
            }

            # Save in DB
            new_user = await user_dao.create_user(db, user_dict)

            # Return as schema
            return UserInfoSchemaBase.model_validate(new_user)
            
    @staticmethod
    async def all_users_list(request: Request) -> SystemUser:
        """
            Add New User.

            :param : No Params Used
            :return: A User object if found, otherwise raises NotFoundError.
        """
        async with async_db_session() as db:
            # token = get_token(request)
            # token_payload = jwt_decode(token).id
            users = await user_dao.all_users_query(db)
            if users:
                return  [UserInfoSchemaBase.model_validate(user) for user in users]
            else:
                return {
                    "code": 400,
                    "msg": "Bad Request",
                    "data": "Invalid Credentials"
                }
            
    @staticmethod
    async def change_password_service(request:Request, obj: ChangePasswordSchema):
        async with async_db_session() as db:
            """
            obj is instance of ChangePasswordSchema
            """
            token = get_token(request)
            user_id = jwt_decode(token).id
            user = await user_dao.get_user_details_by_id(db,user_id=user_id)
            if not user:
                return {
                    "code": 404,
                    "msg": "Not Found",
                    "data": "Customer not found.",
                }
            if not password_verify(obj.current_password, user.usr_password_hash):
                return {
                    "code": 400,
                    "msg": "Bad Request",
                    "data": "Current password is incorrect",
                }

            new_salt = bcrypt.gensalt()
            new_hashed = get_hash_password(obj.new_password, salt=new_salt)
            result = await user_dao.update_user_password(db,user_id,new_hashed)
            if result == 1:
                data = "Password has been updated successfully"
            else:
                data = "Error occurred in password change"
            return data
            
    


    


authservice: AuthService = AuthService()