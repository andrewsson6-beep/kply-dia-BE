from datetime import datetime
from decimal import Decimal
from typing import Optional
from common.schema import SchemaBase


class FamilyResponseSchema(SchemaBase):
    fam_id: int
    fam_unique_no: int
    fam_code: str
    fam_house_name: str
    fam_head_name: str
    fam_phone_number: Optional[str]
    fam_total_contribution_amount: Decimal
    fam_created_at: datetime
    fam_created_by: Optional[int]

    class Config:
        from_attributes = True
        populate_by_name = True

class FamilyCreateSchema(SchemaBase):
    fam_com_id: int
    fam_house_name: str
    fam_head_name: str
    fam_phone_number: Optional[str] = None