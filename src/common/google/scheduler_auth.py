from functools import lru_cache

from fastapi import HTTPException, Request, status
from fastapi.security.utils import get_authorization_scheme_param
from google.auth.transport import requests as google_requests
from google.oauth2 import id_token
from google.cloud import secretmanager

from core.config import settings


@lru_cache
def get_scheduler_service_account_email() -> str:
    if settings.CLOUD_SCHEDULER_SERVICE_ACCOUNT_EMAIL:
        return settings.CLOUD_SCHEDULER_SERVICE_ACCOUNT_EMAIL.strip()

    if not settings.CLOUD_SCHEDULER_SERVICE_ACCOUNT_EMAIL_SECRET_ID:
        raise RuntimeError("Cloud Scheduler service account email is not configured")

    project_id = settings.GOOGLE_SECRET_MANAGER_PROJECT or settings.GOOGLE_CLOUD_PROJECT
    if not project_id:
        raise RuntimeError("Google Cloud project is not configured")

    secret_name = (
        f"projects/{project_id}/secrets/"
        f"{settings.CLOUD_SCHEDULER_SERVICE_ACCOUNT_EMAIL_SECRET_ID}/versions/"
        f"{settings.CLOUD_SCHEDULER_SERVICE_ACCOUNT_EMAIL_SECRET_VERSION}"
    )
    client = secretmanager.SecretManagerServiceClient()
    response = client.access_secret_version(request={"name": secret_name})
    return response.payload.data.decode("utf-8").strip()


async def verify_cloud_scheduler_oidc(request: Request) -> None:
    authorization = request.headers.get("Authorization")
    scheme, token = get_authorization_scheme_param(authorization)

    if not authorization or scheme.lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing Google OIDC bearer token",
        )

    if not settings.CLOUD_SCHEDULER_OIDC_AUDIENCE:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Cloud Scheduler OIDC audience is not configured",
        )

    try:
        token_info = id_token.verify_oauth2_token(
            token,
            google_requests.Request(),
            settings.CLOUD_SCHEDULER_OIDC_AUDIENCE,
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Google OIDC token",
        )

    try:
        expected_email = get_scheduler_service_account_email()
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Cloud Scheduler service account configuration is invalid",
        )

    token_email = token_info.get("email")
    email_verified = token_info.get("email_verified", False)

    if token_email != expected_email or email_verified is not True:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Google OIDC token is not allowed",
        )
