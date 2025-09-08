from fastapi import APIRouter
from src.apps.v1.chat import view as chat_view

api_v1_router = APIRouter()
api_v1_router.include_router(chat_view.router, prefix="/chat", tags=["chat"])