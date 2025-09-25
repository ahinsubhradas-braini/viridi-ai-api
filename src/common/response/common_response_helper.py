from typing import Any

from rich import print

from src.common.response.common_response_model import ResponseModel


async def success_response(
    status: str = "success",
    code: int = 200,
    message: str = "Success",
    data: Any = None,
    module: str = "auth",
):
    print(
        f"[bold green]<========= Common Success api response handler {status, code, message, data, module} ==========> [/bold green]"
    )

    return ResponseModel(
        status="success", status_code=code, message=message, data=data, module=module
    )


async def error_response(
    status: str = "error",
    code: int = 200,
    message: str = "error",
    data: Any = None,
    module: str = "auth",
):
    print(
        f"[bold red]<========= Common Success api response handler {status, code, message, data, module} ==========> [/bold red]"
    )
    return ResponseModel(status="error", status_code=code, message=message, data=data)
