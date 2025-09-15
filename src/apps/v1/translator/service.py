import boto3

async def get_translated_text(data):
    translated_data = data.copy()
    for field in data.fields:
            keys = field.split(".")
            sub_data = translated_data
            for k in keys[:-1]:
                sub_data = sub_data.get(k, {})
            last_key = keys[-1]
            if last_key in sub_data:
                sub_data[last_key] = translate_text(sub_data[last_key], data.source_lang, data.target_lang)

    return translated_data
async def translate_text(text: str, source_lang: str, target_lang: str) -> str:
    if not text:
        return text
    translate_client = boto3.client("translate", region_name="us-east-1")
    response = translate_client.translate_text(
        Text=text,
        SourceLanguageCode=source_lang,
        TargetLanguageCode=target_lang
    )
    return response["TranslatedText"]