from fastapi import APIRouter,Request
from src.common.logger import logger
from src.apps.v1.chat.service import ChatService
router = APIRouter()

@router.get("/sessions")
async def get_sessions(request: Request):
    logger.info("FastAPI app started successfully")
    return {"message": "Sessions data"}

@router.post("/session")
async def session(request:Request):
    await ChatService()
    return {"message":"Session for chatbot"}