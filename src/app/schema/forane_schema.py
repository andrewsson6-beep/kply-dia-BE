from dataclasses import Field
from decimal import Decimal
from typing import List, Optional
from app.schema.community_schema import CommunityResponseSchema
from app.schema.parish_schema import ParishResponseSchema
from common.schema import SchemaBase
from pydantic import Field



class ForaneInfoSchemaBase(SchemaBase):
    """Forane Parameters"""

    forId:int | None  = Field(default=None, description="Forane Id",alias="for_id")
    forCode:str | None =  Field(default=None, description="Forane Code",alias="for_code")
    forName: str | None = Field(default=None, description="Forane Church Name",alias="for_name")
    forLocation:str | None = Field(default=None,  description="Forane Location",alias="for_location")
    forVicarName:str | None  = Field(default=None, description="Forane Vicar Name",alias="for_vicar_name")
    forTotalContribution:Decimal | None  = Field(default=None, description="Forane Total Contribution",alias="for_total_contribution_amount")
    forContactNumber:str | None  = Field(default=None, description="Forane Contact Number",alias="for_contact_number")

    class Config:
        from_attributes = True
        validate_by_name = True



class ForaneParishRequestSchema(SchemaBase):
    """Request schema to fetch parishes under a Forane"""
    foraneId: int = Field(..., alias="forane_id", description="Forane Id")



class ForaneDetailSchema(SchemaBase):
    for_id: int
    for_code: Optional[str]
    for_unique_no: Optional[int]
    for_name: str
    for_location: Optional[str]
    for_vicar_name: Optional[str]
    for_total_contribution_amount: Optional[Decimal] = Field(default=0)
    for_contact_number: Optional[str]
    parishes: List[ParishResponseSchema] = []
    communities: List[CommunityResponseSchema] = []

    class Config:
        from_attributes = True
        populate_by_name = True



class ForaneUpdateSchema(SchemaBase):
    """Schema for updating Forane details"""

    for_id: int = Field(..., description="Forane ID to update")
    for_name: Optional[str] = None
    for_location: Optional[str] = None
    for_vicar_name: Optional[str] = None
    for_contact_number: Optional[str] = None
    for_total_contribution_amount: Optional[Decimal] = None

    class Config:
        from_attributes = True
        populate_by_name = True

class ForaneDeleteSchema(SchemaBase):
    """Schema for deleting a Forane"""
    for_id: int = Field(..., description="Forane ID to delete")
