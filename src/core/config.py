# Import python core libary dependices
import os
from typing import List
# Imports projects or 3rd party libary dependices
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Application Contexts
    application_name: str
    application_description: str
    application_version : str
    cors_origins: List[str]
    application_env: str
    application_url: str
    
    # Swagger creds
    swagger_username: str
    swagger_password: str
    
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
def get_settings():
    return Settings()

settings = Settings()