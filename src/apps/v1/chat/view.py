from fastapi import APIRouter,Request
from src.common.logger import logger
from src.apps.v1.chat.service import ChatService
from src.common.response.stream_response_helper import Stream_response_helper
from fastapi.responses import StreamingResponse

from src.common.security.reate_limiter import limit_request

router = APIRouter()

@router.get("/sessions")
async def get_sessions(request: Request):
    logger.info("FastAPI app started successfully")
    return {"message": "Sessions data"}

@router.post("/session")
@limit_request("1/minute")
async def session(request:Request):
    
    async def event_generator():
        async for event in Stream_response_helper.fake_sse():
            if await request.is_disconnected():
                break
            yield event

    return StreamingResponse(event_generator(), media_type="text/event-stream")