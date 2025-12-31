from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False
    )
    
    database_url: str
    api_title: str = "Expenses Tracker API"
    api_version: str = "1.0.0"


settings = Settings()

