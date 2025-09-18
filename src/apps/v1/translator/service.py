import json

import boto3

from src.core.config import settings
from src.redis_client import redis_cache

translate_client = boto3.client(
    "translate",
    aws_access_key_id=settings.aws_translate_sm_access_key,
    aws_secret_access_key=settings.aws_translate_sm_secret_key,
    region_name=settings.aws_translate_sm_region,
)


async def get_translated_text(data_input, source_lang, target_lang):
    translated_data = data_input.copy()
    translated_data = await translate_fields(translated_data, source_lang, target_lang)
    return translated_data


async def translate_fields(sub_data, source_lang, target_lang):
    """Recursively translate only keys marked as True in fields JSON"""
    for key, value in sub_data.items():
        if key not in sub_data:
            continue
        if isinstance(value, dict) and isinstance(sub_data[key], dict):
            # Nested fields
            sub_data[key] = await translate_fields(
                sub_data[key], value, source_lang, target_lang
            )
        elif value is not None and isinstance(sub_data[key], str):
            # Translate only marked string fields
            sub_data[key] = await translate_text(
                sub_data[key], source_lang, target_lang
            )
    return sub_data


async def translate_text(text: str, source_lang: str, target_lang: str) -> str:
    if not text:
        return text

    print("text", text)
    print("source_lang", source_lang)
    print("target_lang", target_lang)

    try:
        response = translate_client.translate_text(
            Text=text, SourceLanguageCode=source_lang, TargetLanguageCode=target_lang
        )
        print("Translate Done ====>", response)
        return response["TranslatedText"]
    except Exception as e:
        print("Error in translate", e)


async def check_data_exists_in_cache(key):
    try:
        value = redis_cache.get(key)
        print("value", value)
        value = json.loads(value)

        return value
    except Exception as e:
        print("Error in get cache --->", e)


async def set_translated_data_cache(key, data):
    try:
        print("cache_key ===>", key)
        print("data ===>", data)
        data = json.dumps(data)

        value = redis_cache.set(key, data)

        return value
    except Exception as e:
        print("Error in set cache --->", e)


def delete_translated_data_cache(key):
    try:
        redis_cache.delete(key)
    except Exception as e:
        print("Error in delete cache --->", e)


# delete_translated_data_cache("product:2:s-lang:is,t-lang:en")
