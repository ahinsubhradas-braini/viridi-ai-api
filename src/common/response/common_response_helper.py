from typing import Any

from src.common.response.common_response_model import ResponseModel
async def success_response(data: Any = None, message: str = "Success",code:int = 200, status: str = "success"):
    return ResponseModel(status="success",code=code, message=message, data=data)

async def error_response(message: str = "Error",code:int = 200, data: Any = None,status: str = "success"):
    return ResponseModel(status="error",code=code, message=message, data=data)