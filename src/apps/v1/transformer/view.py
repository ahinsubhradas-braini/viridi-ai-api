from fastapi import APIRouter, Depends, Request, Header

from src.apps.v1.transformer.schemas.transformer_schema import (
    CheckHmacRequest,
    TransformRequest,
)
from src.apps.v1.transformer.service import transform_data

# Imports from project or 3rd party libary dependices
from src.common.response.common_response_helper import success_response
from src.common.security.hmac_custom_headers import hmac_headers
from src.common.security.reate_limiter import limit_request
from src.core.config import settings

router = APIRouter()


@router.post("/transform")
@limit_request("5/minute")
async def transform_third_party_data(
    request: Request, body: TransformRequest, headers=Depends(hmac_headers),
    accept_language: str = Header(
        settings.default_locale,  # default value
        description="Language for response, e.g., 'en' or 'is'. Default is English.",
    ),
):
    lang = (
        accept_language.split(",")[0].strip()
        if accept_language
        else settings.default_locale
    )
    get_response = transform_data(body.api_data_url, body.api_provider_name)

     # Get perticular message from header lang

    return await success_response(
        "success",
        200,
        f"{body.api_provider_name} api response transform to unimaze response pattern",
        {"ejs_public_url": get_response},
        "Transformer",
    )


@router.post("/check-hmac")
@limit_request("5/minute")
async def check_hmac(
    request: Request, body: CheckHmacRequest, headers=Depends(hmac_headers)
):
    print("request in check-hmac ==============>", body)
    return await success_response(
        "success", 200, "Check done by hmac checker.", None, "Transformer"
    )
