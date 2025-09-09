# schemas/parish_schema.py
from pydantic import BaseModel, Field
from typing import Optional


class ParishCreateSchema(BaseModel):
    """Request schema to create Parish"""
    parForId: int = Field(..., alias="par_for_id", description="Forane Id reference")
    parCode: Optional[str] = Field(None, alias="par_code", description="Parish Code")
    parName: str = Field(..., alias="par_name", description="Parish Name")
    parLocation: Optional[str] = Field(None, alias="par_location", description="Parish Location")
    parVicarName: Optional[str] = Field(None, alias="par_vicar_name", description="Parish Vicar Name")
    parTotalContribution: Optional[float] = Field(0, alias="par_total_contribution_amount", description="Total Contribution")


class ParishResponseSchema(BaseModel):
    """Response schema for Parish"""
    parId: int = Field(..., alias="par_id")
    parForId: int = Field(..., alias="par_for_id")
    parCode: Optional[str] = Field(None, alias="par_code")
    parName: str = Field(..., alias="par_name")
    parLocation: Optional[str] = Field(None, alias="par_location")
    parVicarName: Optional[str] = Field(None, alias="par_vicar_name")
    parTotalContribution: Optional[float] = Field(0, alias="par_total_contribution_amount")

    class Config:
        from_attributes = True
        populate_by_name = True


