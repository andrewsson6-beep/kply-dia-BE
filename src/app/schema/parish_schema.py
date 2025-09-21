# schemas/parish_schema.py
from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, Field
from typing import List, Optional

from app.schema.community_schema import CommunityResponseSchema
from common.schema import SchemaBase


class ParishCreateSchema(SchemaBase):
    """Request schema to create Parish"""
    parForId: int = Field(..., alias="par_for_id", description="Forane Id reference")
    parCode: Optional[str] = Field(None, alias="par_code", description="Parish Code")
    parName: str = Field(..., alias="par_name", description="Parish Name")
    parLocation: Optional[str] = Field(None, alias="par_location", description="Parish Location")
    parVicarName: Optional[str] = Field(None, alias="par_vicar_name", description="Parish Vicar Name")
    parTotalContribution: Optional[float] = Field(0, alias="par_total_contribution_amount", description="Total Contribution")
    parContactNumber:str | None  = Field(default=None, description="parish Contact Number",alias="par_contact_number")


class ParishResponseSchema(SchemaBase):
    """Response schema for Parish"""
    parId: int = Field(..., alias="par_id")
    parForId: int = Field(..., alias="par_for_id")
    parCode: Optional[str] = Field(None, alias="par_code")
    parUniqueNo: Optional[int] = Field(None, alias="par_unique_no")
    parName: str = Field(..., alias="par_name")
    parLocation: Optional[str] = Field(None, alias="par_location")
    parVicarName: Optional[str] = Field(None, alias="par_vicar_name")
    parTotalContribution: Optional[float] = Field(0, alias="par_total_contribution_amount")
    parContactNumber: Optional[str] = Field(None, alias="par_contact_number")


    class Config:
        from_attributes = True
        populate_by_name = True


class ParishBaseSchema(SchemaBase):
    par_code: Optional[str] = None
    par_name: Optional[str] = None
    par_location: Optional[str] = None
    par_vicar_name: Optional[str] = None
    par_contact_number: Optional[str] = None


class ParishUpdateSchema(ParishBaseSchema):
    par_id: int

class ParishRequestSchema(SchemaBase):
    par_id: int



class ParishDetailSchema(ParishBaseSchema):
    par_id: int
    par_for_id: int
    par_total_contribution_amount: Decimal
    par_created_at: datetime
    par_updated_at: Optional[datetime] = None
    communities: List[CommunityResponseSchema] = []


    class Config:
        from_attributes = True
    






