from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "ClinIQ AI"
    environment: str = "development"
    api_prefix: str = "/api/v1"
    openai_api_key: str = ""
    openai_model: str = "gpt-4o-mini"
    pinecone_api_key: str = ""
    pinecone_index: str = "cliniq-medical"
    pinecone_cloud: str = "aws"
    pinecone_region: str = "us-east-1"
    postgres_dsn: str = "postgresql+psycopg://cliniq:cliniq@localhost:5432/cliniq"
    redis_url: str = "redis://localhost:6379/0"
    jwt_secret: str = "change_me"
    jwt_algorithm: str = "HS256"
    log_level: str = "INFO"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


settings = Settings()
