
from fastapi import APIRouter,Request
# Imports from project or 3rd party libary dependices
from src.common.response.common_response_helper import success_response
from src.common.security.reate_limiter import limit_request
from src.apps.v1.transformer.schemas.transformer_schema import CheckHmacRequest, TransformRequest
from src.apps.v1.transformer.service import transform_data

router = APIRouter()

@router.post("/transform")
@limit_request("5/minute")
async def transform_third_party_data(request: Request, body: TransformRequest):
    
    get_response = transform_data(body.api_data_url,body.api_provider_name)

    return await success_response("success",200,f"{body.api_provider_name} api response transform to unimaze response pattern",{"ejs_public_url": get_response},"Transformer")

@router.post("/check-hmac")
@limit_request("5/minute")
async def check_hmac(request:Request,body: CheckHmacRequest):
    print("request in check-hmac ==============>",body)
    return await success_response("success",200,"Check done by hmac checker.",None,"Transformer")