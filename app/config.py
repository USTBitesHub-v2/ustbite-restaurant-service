from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_env: str = "local"
    database_url: str = ""
    rabbitmq_url: str = ""
    redis_url: str = ""
    AWS_REGION: str = "us-east-1"
    BEDROCK_EMBED_MODEL_ID: str = "amazon.titan-embed-text-v2:0"

    class Config:
        env_file = ".env"

settings = Settings()
