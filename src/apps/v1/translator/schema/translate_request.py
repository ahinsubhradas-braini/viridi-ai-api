from pydantic import BaseModel
from typing import Optional

class TranslateRequest(BaseModel):
    module_name: str
    module_id: str
    source_lang: str   # dynamic
    target_lang: str   # dynamic
    source_data: dict