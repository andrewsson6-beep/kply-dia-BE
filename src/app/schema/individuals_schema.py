from dataclasses import Field
from common.schema import SchemaBase
from pydantic import Field


class IndividualsInfoSchemaBase(SchemaBase):
    """Individuals Parameters"""

    indId:int | None  = Field(default=None, description="Individual Id",alias="ind_id")
    indUniqueNo:str | None =  Field(default=None, description=" Individual Unique Number",alias="ind_unique_no")
    indCode: str | None = Field(default=None, description="Individual Code",alias="ind_code")
    indFullName:int | None = Field(default=None,  description="Individual Full Name",alias="ind_full_name")
    indPhoneNumber:str | None  = Field(default=None, description="Individual Phone Number",alias="ind_phone_number")
    indEmail:str | None  = Field(default=None, description="Individual Email Address",alias="ind_email")
    indAddress:str | None  = Field(default=None, description="Individual Address",alias="ind_address")
    indContributionAmount: str | None = Field(default=None, description="Individual Total Contribution Amount",alias="ind_total_contribution_amount")


    class Config:
        from_attributes = True
        validate_by_name = True