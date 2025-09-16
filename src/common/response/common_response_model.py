# Import python core libary dependices
from typing import Any, Optional

# Imports projects or 3rd party libary dependices
from pydantic import BaseModel

class ResponseModel(BaseModel):
    status: str          # "success" / "error"
    status_code: int
    message: str
    data: Optional[Any]  # can hold anything (dict, list, str, etc.)
    module: Any