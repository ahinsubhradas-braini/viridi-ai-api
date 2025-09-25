def get_message(module_messages: dict, key: str, lang: str):
    # Fallback to English if language not found
    return module_messages.get(lang, module_messages.get("en", {})).get(key, key)
