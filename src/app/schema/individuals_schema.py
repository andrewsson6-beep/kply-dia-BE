from dataclasses import Field
from decimal import Decimal
from typing import List, Optional
from app.schema.contribution_schema import IndividualContributionResponseSchema
from common.schema import SchemaBase
from pydantic import Field


class IndividualsInfoSchemaBase(SchemaBase):
    """Individuals Parameters"""

    indId:int | None  = Field(default=None, description="Individual Id",alias="ind_id")
   
    indFullName:str | None = Field(default=None,  description="Individual Full Name",alias="ind_full_name")
    indPhoneNumber:str | None  = Field(default=None, description="Individual Phone Number",alias="ind_phone_number")
    indEmail:str | None  = Field(default=None, description="Individual Email Address",alias="ind_email")
    indAddress:str | None  = Field(default=None, description="Individual Address",alias="ind_address")
    indContributionAmount: Decimal | None = Field(default=None, description="Individual Total Contribution Amount",alias="ind_total_contribution_amount")


    class Config:
        from_attributes = True
        validate_by_name = True



class IndividualDetailSchema(SchemaBase):
    ind_id: int
    ind_code: Optional[str]
    ind_unique_no:Optional[int]
    ind_full_name: str
    ind_phone_number: Optional[str]
    ind_email: Optional[str]
    ind_address: Optional[str]
    ind_total_contribution_amount: Decimal = Field(..., alias="ind_total_contribution_amount")
    contributions: List[IndividualContributionResponseSchema] = []

    class Config:
        from_attributes = True
        populate_by_name = True

class IndividualDetailRequestSchema(SchemaBase):
    individualId: int = Field(..., alias="ind_id", description="Individual ID")



class IndividualUpdateSchema(SchemaBase):
    ind_id: int = Field(..., description="Individual ID to update")
    ind_full_name: Optional[str] = None
    ind_phone_number: Optional[str] = None
    ind_email: Optional[str] = None
    ind_address: Optional[str] = None

    class Config:
        from_attributes = True
        populate_by_name = True