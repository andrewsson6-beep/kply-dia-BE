from datetime import date
from decimal import Decimal
from typing import Literal, Optional

from common.schema import SchemaBase
from pydantic import Field


ContributionReportEntityType = Literal[
    "family",
    "parish",
    "forane",
    "individual",
    "institution",
]


class ContributionReportRequestSchema(SchemaBase):
    entityType: ContributionReportEntityType = Field(
        ...,
        alias="entity_type",
        description="Report entity type",
    )
    entityId: int = Field(..., alias="entity_id", description="Report entity ID")
    year: Optional[int] = Field(None, description="Single report year")
    fromYear: Optional[int] = Field(None, alias="from_year", description="Start report year")
    toYear: Optional[int] = Field(None, alias="to_year", description="End report year")


class ContributionReportPeriodSchema(SchemaBase):
    from_year: int
    to_year: int
    from_date: date
    to_date: date


class ContributionReportEntitySchema(SchemaBase):
    type: str
    id: int
    code: Optional[str] = None
    name: Optional[str] = None


class ContributionReportSummarySchema(SchemaBase):
    total_amount: Decimal
    total_count: int


class ContributionReportResponseSchema(SchemaBase):
    period: ContributionReportPeriodSchema
    entity: ContributionReportEntitySchema
    summary: ContributionReportSummarySchema
    contributions: list[dict]
