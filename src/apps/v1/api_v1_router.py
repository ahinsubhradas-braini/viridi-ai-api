from fastapi import APIRouter
from src.apps.v1.chat import view as chat_view
from src.apps.v1.transformer import view as transformer_view

api_v1_router = APIRouter()

api_v1_router.include_router(transformer_view.router, prefix="/ai-transformer", tags=["Ai-transformer"]) # Route for transformer
api_v1_router.include_router(chat_view.router, prefix="/chat", tags=["chat"]) # Route for chatbot
