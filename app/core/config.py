from pydantic_settings import BaseSettings
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Setting(BaseSettings):
    api_v1_prefix: str = "/api/v1"
    db_URL: str = Field(..., alias="DB_URL")
    db_echo: bool = Field(..., alias="DB_ECHO")
    secret_key: str = Field(..., alias="SECRET_KEY")

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Setting()