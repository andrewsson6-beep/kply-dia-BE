
from datetime import datetime
from decimal import Decimal
from typing import Optional
from common.schema import SchemaBase
from pydantic import Field


class FamilyResponseSchema(SchemaBase):
    fam_id: int
    fam_unique_no: int
    fam_code: str
    fam_house_name: str
    fam_head_name: str
    fam_phone_number: Optional[str]
    fam_total_contribution_amount: Decimal


    class Config:
        from_attributes = True
        populate_by_name = True

class FamilyCreateSchema(SchemaBase):
    fam_com_id: int
    fam_house_name: str
    fam_head_name: str
    fam_phone_number: Optional[str] = None


class FamilyUpdateSchema(SchemaBase):
    fam_id: int = Field(..., description="Family ID to update")
    fam_house_name: Optional[str] = None
    fam_head_name: Optional[str] = None
    fam_phone_number: Optional[str] = None
    fam_total_contribution_amount: Optional[Decimal] = None