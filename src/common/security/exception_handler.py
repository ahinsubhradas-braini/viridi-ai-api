# from fastapi import Request, HTTPException
# from fastapi.responses import JSONResponse
# from fastapi.exceptions import RequestValidationError
# from pydantic import BaseModel
# import logging

# class ExceptionHandlersMixin:
#     """All exception handlers in one mixin with unified response structure."""
#     @staticmethod
#     def _build_response(status: str, code: int, message: str, data=None,type: str =None):
#         print("status ===>",status)
#         print("code ===>",code)
#         print("message ===>",message)
#         print("data ===>",data)
#         print("type ===>",type)

#         return JSONResponse(
#             status_code=code,
#             content={
#                 "status":status,
#                 "status_code":code,
#                 "message":message,
#                 "data":data
#             }
#         )
#     @staticmethod
#     async def http_exception_handler(request: Request, exc: HTTPException):
#         logging.warning(f"HTTPException: {exc.detail} at {request.url.path}")
#         return ExceptionHandlersMixin._build_response(status="error", code=exc.status_code, message=str(exc.detail),data=None,type="Http Exception")
#     @staticmethod
#     async def validation_exception_handler(request: Request, exc: RequestValidationError):
#         logging.info(f"Validation error at {request.url.path}: {exc.errors()}")
#         return ExceptionHandlersMixin._build_response(status="error", code=422, message="Validation error", data={"errors": exc.errors()},type="Validation Error")
#     @staticmethod
#     async def value_error_handler(request: Request, exc: ValueError):
#         logging.info(f"ValueError at {request.url.path}: {str(exc)}")
#         return ExceptionHandlersMixin._build_response(status="error",code=400,message=str(exc),data=None,type="Value Error" )
