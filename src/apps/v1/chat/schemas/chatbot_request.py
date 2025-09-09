from pydantic import BaseModel
from typing import Optional

class SessionRequest(BaseModel):
    user_query: str
    user_id: str
    user_name: str
    # session_id : Optional[str]