from typing import Any

from src.common.response.common_response_model import ResponseModel
async def success_response(status: str = "success",code:int = 200,message: str = "Success",data: Any = None,type:str="success"):

    print(status)
    print(code)
    print(message)
    print(data)
    print("22222",type)
    return ResponseModel(status="success",status_code=code, message=message, data=data)

async def error_response(status: str = "error",code:int = 200,message: str = "error",data: Any = None,type:str="success"):
    return ResponseModel(status="error",status_code=code, message=message, data=data)