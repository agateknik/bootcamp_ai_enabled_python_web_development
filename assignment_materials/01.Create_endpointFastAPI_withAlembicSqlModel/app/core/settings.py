from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "Task App"
    VERSION: str = "0.0.1"
    
settings = Settings()
