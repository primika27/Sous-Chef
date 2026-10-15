from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "SousChef Engine"
    API_V1_PREFIX: str = "/api/v1"
    
    # AI Credentials
    GEMINI_API_KEY: str

    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8", 
        extra="ignore"
    )

settings = Settings()