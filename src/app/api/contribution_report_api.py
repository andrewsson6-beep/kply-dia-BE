from fastapi import APIRouter

from app.schema.contribution_report_schema import ContributionReportRequestSchema
from app.service.contribution_report_service import contributionreportservice
from common.response.response_schema import ResponseSchemaModel, response_base
from common.security.jwt import DependsJwtAuth
from common.exception.errors import TokenError

router = APIRouter()


@router.post("/contribution-report", dependencies=[DependsJwtAuth])
async def contribution_report(data: ContributionReportRequestSchema) -> ResponseSchemaModel:
    try:
        report = await contributionreportservice.get_contribution_report(data)
        return response_base.success(data=report)
    except ValueError as e:
        return response_base.fail(data=str(e))
    except TokenError as e:
        raise e
    except Exception as e:
        return response_base.fail(data=f"Something went wrong: {str(e)}")
