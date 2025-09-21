from dataclasses import Field
from datetime import datetime
from decimal import Decimal
from typing import List, Optional
from app.schema.contribution_schema import InstitutionContributionResponseSchema
from common.schema import SchemaBase
from pydantic import Field


class InstitutionsInfoSchemaBase(SchemaBase):
    """Institutions Parameters"""

    insId:int | None  = Field(default=None, description="Institution Id",alias="ins_id")
    # insForId:int | None =  Field(default=None, description=" Institution Forane Id",alias="ins_for_id")
    # insParId: int | None = Field(default=None, description="Institution Parish Id",alias="ins_par_id")
    # insUniqueNo:int | None = Field(default=None,  description="Institution Unique Number",alias="ins_unique_no")
    # insCode:str | None  = Field(default=None, description="Institution Code",alias="ins_code")
    insName:str | None  = Field(default=None, description="Institution Name",alias="ins_name")
    insType:str | None  = Field(default=None, description="Institution Type",alias="ins_type")
    insAddress: str | None = Field(default=None, description="Institution Address",alias="ins_address")
    insPhone:str | None = Field(default=None,  description="Institution Phone",alias="ins_phone")
    insEmail:str | None  = Field(default=None, description="Institution Email Address",alias="ins_email")
    insWebsite:str | None  = Field(default=None, description="Institution Website",alias="ins_website")
    insHeadName:str | None  = Field(default=None, description="Institution Head Name",alias="ins_head_name")
    insContributionAmount: Decimal | None = Field(..., alias="ins_total_contribution_amount")
    
    class Config:
        from_attributes = True
        validate_by_name = True




class InstitutionDetailSchema(InstitutionsInfoSchemaBase):

    contributions: List[InstitutionContributionResponseSchema] = []

    class Config:
        from_attributes = True
        populate_by_name = True

class InstitutionDetailRequestSchema(SchemaBase):
    institutionId: int = Field(..., alias="ins_id", description="Institution ID")



class InstitutionUpdateSchema(SchemaBase):
    """Schema for updating institution details"""

    ins_id: int = Field(..., description="Institution ID to update")
    ins_name: Optional[str] = None
    ins_type: Optional[str] = None
    ins_address: Optional[str] = None
    ins_phone: Optional[str] = None
    ins_email: Optional[str] = None
    ins_website: Optional[str] = None
    ins_head_name: Optional[str] = None
    


    class Config:
        from_attributes = True
        populate_by_name = True

