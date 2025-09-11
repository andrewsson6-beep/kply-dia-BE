from datetime import datetime
from decimal import Decimal
from typing import Optional
from common.schema import SchemaBase
from pydantic import Field



# Individual Contribution Schemas
# ------------------------------------

class IndividualContributionCreateSchema(SchemaBase):
    """Request schema for creating a contribution"""
    individualId: int = Field(..., alias="icon_ind_id", description="Individual ID")
    amount: float = Field(..., alias="icon_amount", description="Contribution Amount")
    purpose: Optional[str] = Field(None, alias="icon_purpose", description="Contribution Purpose")


class IndividualContributionResponseSchema(SchemaBase):
    """Response schema for a contribution"""
    icon_id: int
    icon_ind_id: int
    icon_amount: float
    icon_date: datetime
    icon_purpose: Optional[str]

    class Config:
        from_attributes = True
        populate_by_name = True


class IndividualContributionUpdateSchema(SchemaBase):
    icon_id: int = Field(..., description="Contribution ID to update")
    icon_amount: Optional[Decimal] = None
    icon_date: Optional[datetime] = None
    icon_purpose: Optional[str] = None

    class Config:
        from_attributes = True
        populate_by_name = True




# Instituttion Contribution Schemas
# ------------------------------------


class InstitutionContributionCreateSchema(SchemaBase):
    """Request schema for creating a contribution"""
    institutionId: int = Field(..., alias="incon_ins_id", description="Institution ID")
    amount: float = Field(..., alias="incon_amount", description="Contribution Amount")
    purpose: Optional[str] = Field(None, alias="incon_purpose", description="Contribution Purpose")


class InstitutionContributionResponseSchema(SchemaBase):
    incon_id: int
    incon_ins_id: int
    incon_amount: Decimal
    incon_date: datetime
    incon_purpose: Optional[str]

    class Config:
        from_attributes = True
        populate_by_name = True


class InstitutionContributionUpdateSchema(SchemaBase):
    """Schema for updating institution contributions"""

    incon_id: int = Field(..., description="Contribution ID to update")
    incon_amount: Optional[Decimal] = None
    incon_purpose: Optional[str] = None

    class Config:
        from_attributes = True
        populate_by_name = True


class InstitutionContributionResponseSchema(SchemaBase):
    """Response schema for institution contributions"""

    incon_id: int
    incon_ins_id: int
    incon_amount: Decimal
    incon_date: datetime
    incon_purpose: Optional[str]

    class Config:
        from_attributes = True
        populate_by_name = True

