from datetime import date, datetime
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
    contributionDate: Optional[date] = Field(None, alias="icon_date")

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
    icon_date: Optional[date] = None
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
    institutionContributionDate: Optional[date] = Field(None, alias="incon_date", description="Contribution Purpose")

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
    ins_updated_at: Optional[datetime] = None
    incon_date: Optional[date] = None
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



# Family Contribution Schemas
# ------------------------------------


class FamilContributionCreateSchema(SchemaBase):
    """Request schema for creating a contribution"""
    familyId: int = Field(..., alias="fcon_fam_id", description="Family ID")
    amount: float = Field(..., alias="fcon_amount", description="Contribution Amount")
    purpose: Optional[str] = Field(None, alias="fcon_purpose", description="Contribution Purpose")
    familyContributionDate: Optional[date] = Field(None, alias="fcon_date", description="Contribution Date")

class FamilContributionResponseSchema(SchemaBase):
    fcon_id: int
    fcon_fam_id: int
    fcon_amount: Decimal
    fcon_date: datetime
    fcon_purpose: Optional[str]

    class Config:
        from_attributes = True
        populate_by_name = True


class FamilContributionUpdateSchema(SchemaBase):
    """Schema for updating family contributions"""

    fcon_id: int = Field(..., description="Contribution ID to update")
    fcon_amount: Optional[Decimal] = None
    fcon_purpose: Optional[str] = None
    fcon_date: Optional[date] = None 

    class Config:
        from_attributes = True
        populate_by_name = True

class FamilContributionDeleteSchema(SchemaBase):
    """Schema for deleting family contributions"""
    fcon_id: int

