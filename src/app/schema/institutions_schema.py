from dataclasses import Field
from common.schema import SchemaBase
from pydantic import Field


class InstitutionsInfoSchemaBase(SchemaBase):
    """Institutions Parameters"""

    insId:int | None  = Field(default=None, description="Institution Id",alias="ins_id")
    insForId:str | None =  Field(default=None, description=" Institution Forane Id",alias="ins_for_id")
    insParId: str | None = Field(default=None, description="Institution Parish Id",alias="ins_par_id")
    insUniqueNo:int | None = Field(default=None,  description="Institution Unique Number",alias="ins_unique_no")
    insCode:str | None  = Field(default=None, description="Institution Code",alias="ins_code")
    insName:str | None  = Field(default=None, description="Institution Name",alias="ins_name")
    insType:str | None  = Field(default=None, description="Institution Type",alias="ins_type")
    insAddress: str | None = Field(default=None, description="Institution Address",alias="ins_address")
    insPhone:int | None = Field(default=None,  description="Institution Phone",alias="ins_phone")
    insEmail:str | None  = Field(default=None, description="Institution Email Address",alias="ins_email")
    insWebsite:str | None  = Field(default=None, description="Institution Website",alias="ins_website")
    insHeadName:str | None  = Field(default=None, description="Institution Head Name",alias="ins_head_name")
    
    class Config:
        from_attributes = True
        validate_by_name = True