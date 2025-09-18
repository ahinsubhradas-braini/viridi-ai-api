from pydantic import BaseModel


class TransformRequest(BaseModel):
    api_data_url: str
    api_provider_name: str


class CheckHmacRequest(BaseModel):
    userId: int
    action: str
