from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    REDIS_URL: str
    WEATHER_API_KEY: str

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding='utf-8')

# Create a singleton instance to be used across the app
settings = Settings()