from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    APP_NAME: str = "Trabalho 3 - FastAPI + Mongo"
    MONGODB_URL: str
    DATABASE_NAME: str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
