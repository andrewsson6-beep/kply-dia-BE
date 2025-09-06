from dataclasses import Field
from common.schema import SchemaBase
from pydantic import Field



class ForaneInfoSchemaBase(SchemaBase):
    """Forane Parameters"""

    forId:int | None  = Field(default=None, description="Forane Id",alias="for_id")
    forCode:str | None =  Field(default=None, description="Forane Code",alias="for_code")
    forName: str | None = Field(default=None, description="Forane Church Name",alias="for_name")
    forLocation:str | None = Field(default=None,  description="Forane Location",alias="for_location")
    forVicarName:str | None  = Field(default=None, description="Forane Vicar Name",alias="for_vicar_name")
    forTotalContribution:int | None  = Field(default=None, description="Forane Total Contribution",alias="for_total_contribution_amount")
    forContactNumber:str | None  = Field(default=None, description="Forane Contact Number",alias="for_contact_number")

    class Config:
        from_attributes = True
        validate_by_name = True