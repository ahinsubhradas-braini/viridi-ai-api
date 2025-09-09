import asyncio
from fastapi import APIRouter,Request
from src.apps.v1.chat.schemas.chatbot_request import SessionRequest
from src.common.logger import logger
from src.apps.v1.chat.service import ChatService
from src.common.response.stream_response_helper import Stream_response_helper
from fastapi.responses import StreamingResponse

from src.common.security.reate_limiter import limit_request
from src.apps.v1.chat.intent_model import predict_intent
router = APIRouter()

@router.get("/sessions")
async def get_sessions(request: Request):
    logger.info("FastAPI app started successfully")
    return {"message": "Sessions data"}

@router.post("/session")
@limit_request("1/minute")
async def session(request:Request,session_data: SessionRequest):
    check_prediction_intent = await asyncio.to_thread(predict_intent, session_data.user_query, 0.5)
    print("check_prediction_intent",check_prediction_intent)
    if(check_prediction_intent['score'] < 0.5 or check_prediction_intent['intent'] == 'out_of_domain'):
        return {"message": "Out of domain query detected. Please ask a relevant question."}
    else:
        async def event_generator():
            async for event in Stream_response_helper.fake_sse():
                yield event

        return StreamingResponse(event_generator(), media_type="text/event-stream")