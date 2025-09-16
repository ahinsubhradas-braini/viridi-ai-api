# Import python core libary dependices
from contextlib import asynccontextmanager

# Imports fastapi dependices
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from src.common.security.hmac_checker import hmac_auth_middleware
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.responses import JSONResponse

# Imports from project or 3rd party libary dependices
from src.apps.v1.api_v1_router import api_v1_router
from src.core.config import get_settings
from src.common.response.common_response_helper import success_response
from slowapi.middleware import SlowAPIMiddleware
from src.common.security.reate_limiter import limiter, rate_limit_exceeded_handler

# Set settings
settings = get_settings()

# Lifespan event handlers
# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     print("Lifespan event starting")

# Fastapi application creation
app = FastAPI(
    title = settings.application_name,
    description = settings.application_description,
    version = settings.application_version,
    contact={
        "name": "Contact us",
        "url": "https://viridi-ai.mydevfactory.com",
        "email": "ahin.subhra.das@brainiuminfotech.com",
    },
    docs_url=None, # Disable deafult docs url for swagger
    redoc_url=None,
    # lifespan=lifespan
)

# Allow cors origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rate limiter middleware
app.add_middleware(SlowAPIMiddleware)
app.state.limiter = limiter
app.add_exception_handler(429, rate_limit_exceeded_handler)

# Add hmac middleware for security
class CustomHmacMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
            try:
            # Call the hmac checker to check signature key
                await hmac_auth_middleware(request)
                response = await call_next(request)
                return response
            except Exception as exc:
            # If token validation fails due to other exceptions, return a generic error response
                return JSONResponse(content={"detail": f"Error: {str(exc)}"}, status_code=500)
        
app.add_middleware(CustomHmacMiddleware)

# Root Handeling: If any user trigger base api endpoint it will send this json
@app.get("/",include_in_schema=False)
async def root():
    return await success_response(
        status="success",
        code= 200,
        data={
            "message": f"Hello from {settings.application_name},please check {settings.application_url}",
            "environment": settings.application_env,
            "application_name": settings.application_name,
        },
        message="Welcome to API",
        type= "Success"
    )

""" 
Adding security in swagger api docs start here
"""
security = HTTPBasic()

# Verify credentials what user will give in the time of opening swagger docs
async def verify_credentials(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = settings.swagger_username
    correct_password = settings.swagger_password

    if not (credentials.username == correct_username and credentials.password == correct_password):
        print("<========= Invalid Swagger credentials ==============>")
    return True

# Protect Swagger UI
@app.get("/docs", include_in_schema=False)
async def get_documentation(_: bool = Depends(verify_credentials)):
    return get_swagger_ui_html(openapi_url="/openapi.json", title="Secure Docs",init_oauth={
            "additionalQueryStringParams": {
                "x-request-from": "swagger-ui"
            }
        })

# Protect OpenAPI schema too
@app.get("/openapi.json", include_in_schema=False)
async def openapi(_: bool = Depends(verify_credentials)):
    return get_openapi(title="My API", version="1.0.0", routes=app.routes)

"""
 Adding security in swagger api docs end here
"""

# Include routers
app.include_router(api_v1_router, prefix="/api/v1")