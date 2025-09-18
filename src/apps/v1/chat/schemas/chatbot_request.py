from pydantic import BaseModel


class SessionRequest(BaseModel):
    user_query: str
    user_id: int
    user_name: str
    # session_id : Optional[str]
