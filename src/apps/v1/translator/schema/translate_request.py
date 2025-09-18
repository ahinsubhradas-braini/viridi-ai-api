from pydantic import BaseModel


class TranslateRequest(BaseModel):
    module_name: str
    module_id: str
    source_lang: str  # dynamic
    target_lang: str  # dynamic
    source_data: dict
