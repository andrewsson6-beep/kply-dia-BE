from dataclasses import Field
from datetime import datetime
from typing import Optional

from common.schema import SchemaBase
from pydantic import Field



class UserInfoSchemaBase(SchemaBase):
    """System Level User Parameters"""

    userId:int | None  = Field(default=None, description="User Id",alias="usr_id")
    userName:str | None =  Field(default=None, description="User Name",alias="usr_username")
    userEmail: str | None = Field(default=None, description="User Email",alias="usr_email")
    userRoleId:int | None = Field(default=None,  description="Role ID",alias="usr_rol_id")
    userPassword:str | None  = Field(default=None, description="User Password",alias="usr_password")

    class Config:
        from_attributes = True
        validate_by_name = True

   

class UserCreateSchema(SchemaBase):
    userName: str = Field(alias="usr_username")
    userEmail: str = Field(alias="usr_email")
    userRoleId: int = Field(alias="usr_rol_id")
    userPassword: str = Field(alias="usr_password")  # required


    class Config:
        from_attributes = True
        validate_by_name = True


