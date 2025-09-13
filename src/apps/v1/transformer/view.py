
from fastapi import APIRouter,Request
# Imports from project or 3rd party libary dependices
from src.common.security.reate_limiter import limit_request
from src.apps.v1.transformer.schemas.transformer_schema import TransformRequest
from src.apps.v1.transformer.service import transform_data

router = APIRouter()

@router.post("/transform")
@limit_request("5/minute")
def transform_third_party_data(request: Request, body: TransformRequest):
    
    get_response = transform_data(body.api_data_url,body.api_provider_name)

    return {"message": "Transform data", "data": {
        "message": f"{body.api_provider_name} api response transform to unimaze response pattern",
        "ejs_public_url": get_response
    }}