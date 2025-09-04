from datetime import datetime
from typing import List, Optional
from common.schema import SchemaBase
from pydantic import Field
from typing_extensions import Self
from app.schema.user_schema import UserInfoSchemaBase
from common.dataclasses import AccessToken



class LoginSchemaBase(SchemaBase):
    """Authentication Parameters"""

    useremail: str = Field(description="email")
    userpassword: str | None = Field(description="password")


class UserAuthenticatedDetails(UserInfoSchemaBase,AccessToken):
    """User Authenticated Details"""



class ChangePasswordSchema(SchemaBase):
    current_password: str = Field(..., min_length=6)
    new_password: str = Field(..., min_length=6)

   