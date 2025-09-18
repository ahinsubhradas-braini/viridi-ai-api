# Import python core libary dependices
from typing import List

# Imports projects or 3rd party libary dependices
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Application Contexts
    application_name: str
    application_description: str
    application_version: str
    cors_origins: List[str]
    application_env: str
    application_url: str
    port: int

    # Swagger creds
    swagger_username: str
    swagger_password: str

    # Vridi primary application database
    db_user: str
    db_pass: str
    db_host: str
    db_name: str

    # Llm creds
    open_router_key: str
    open_router_url: str
    open_router_model: str
    llm_timeout: int

    # Aws s3 creds
    aws_access_key: str
    aws_secret_key: str
    aws_region: str
    viridi_ai_bucket_name: str

    # Aws translate & secret manager key
    aws_translate_sm_access_key: str
    aws_translate_sm_secret_key: str
    aws_translate_sm_region: str

    # Aws secret key names
    aws_sm_secret_name: str

    aws_sm_hmac_secret_key_name: str

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


def get_settings():
    return Settings()


settings = Settings()
