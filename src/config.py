from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    BOT_TOKEN: str
    LOG_LEVEL: str
    LOG_FORMAT: str

    model_config = SettingsConfigDict(env_file=".env")
