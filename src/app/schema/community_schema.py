from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, Field
from pydantic import model_validator
from typing import List, Optional

from app.schema.family_schema import FamilyResponseSchema
from common.schema import SchemaBase

class CommunityCreateSchema(SchemaBase):
    com_for_id: Optional[int] = Field(default=None, description="Forane ID if community belongs to a Forane")
    com_par_id: Optional[int] = Field(default=None, description="Parish ID if community belongs to a Parish")
    com_name: str = Field(..., description="Community name")

    @model_validator(mode="after")
    def validate_parent_choice(self):
        # Exactly one of com_for_id or com_par_id must be provided
        if (self.com_for_id is None and self.com_par_id is None) or (
            self.com_for_id is not None and self.com_par_id is not None
        ):
            raise ValueError("Provide exactly one of 'com_for_id' or 'com_par_id', not both or neither.")
        return self



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

    @model_validator(mode="after")
    def validate_parent_choice(self):
        # For updates, allow neither to be provided (no change), but disallow both being set simultaneously
        if self.com_for_id is not None and self.com_par_id is not None:
            raise ValueError("Provide only one of 'com_for_id' or 'com_par_id' when updating, not both.")
        return self

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


