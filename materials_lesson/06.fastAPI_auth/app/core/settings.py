from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "Task App"
    VERSION: str = "0.0.1"
    SECRET_KEY: str = "verysecretjoss"

    # exp token
    JWT_EXP_MINUTES: int = 5
    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
