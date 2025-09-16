from fastapi import HTTPException
import uuid
from src.apps.v1.translator.language_constants import SUPPORTED_LANGUAGES
from src.apps.v1.translator.schema.translate_request import TranslateRequest
from src.apps.v1.translator.service import get_translated_text
from fastapi import APIRouter,Request

router = APIRouter()

@router.post("/translate")
async def translate_module(req: TranslateRequest):
    # Validate languages
    if not is_supported_language(req.source_lang):
        raise HTTPException(status_code=400, detail=f"Source language '{req.source_lang}' not supported")
    if not is_supported_language(req.target_lang):
        raise HTTPException(status_code=400, detail=f"Target language '{req.target_lang}' not supported")
    
    # Generate request_id
    request_id = str(uuid.uuid4())

    # Cache key for module + id + target_lang
    # cache_key = f"{req.module_name}:{req.module_id}:lang:{req.target_lang}"
    # Save to cache
    translated_data = await get_translated_text(req.source_data,req.source_lang,req.target_lang)
    return {"request_id": request_id, "translated_data": translated_data}

def is_supported_language(lang_code: str) -> bool:
    return lang_code in SUPPORTED_LANGUAGES