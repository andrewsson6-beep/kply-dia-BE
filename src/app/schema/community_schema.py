from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, Field
from typing import List, Optional

from app.schema.family_schema import FamilyResponseSchema
from common.schema import SchemaBase

class CommunityCreateSchema(SchemaBase):
    com_for_id: Optional[int] = Field(default=None, description="Forane ID if community belongs to a Forane")
    com_par_id: Optional[int] = Field(default=None, description="Parish ID if community belongs to a Parish")
    com_name: str = Field(..., description="Community name")



class CommunityResponseSchema(BaseModel):
    com_id: int
    com_for_id: Optional[int]
    com_par_id: Optional[int]
    com_unique_no: int
    com_code: str
    com_name: str
    com_total_contribution_amount: Decimal
    com_created_at: datetime
    com_created_by: Optional[int]

    class Config:
        from_attributes = True  # allows ORM to Schema mapping
        populate_by_name = True


class CommunityUpdateSchema(BaseModel):
    com_id: int = Field(..., description="Community ID to update")
    com_name: Optional[str] = None
    com_for_id: Optional[int] = None
    com_par_id: Optional[int] = None
    com_total_contribution_amount: Optional[float] = None
    com_updated_by: Optional[int] = None

    class Config:
        from_attributes = True
        populate_by_name = True


class CommunityListRequestSchema(SchemaBase):
    forane_id: Optional[int] = None
    parish_id: Optional[int] = None

class CommunityDetailSchema(SchemaBase):
    com_id: int
    com_for_id: Optional[int]
    com_par_id: Optional[int]
    com_unique_no: int
    com_code: str
    com_name: str
    com_total_contribution_amount: Decimal
    families: List[FamilyResponseSchema] = []

    class Config:
        from_attributes = True
        populate_by_name = True


class CommunityRequestSchema(SchemaBase):
    com_id: int


