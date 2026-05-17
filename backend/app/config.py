from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # Supabase
    supabase_url: str
    supabase_anon_key: str
    supabase_service_role_key: str
    database_url: str

    # Groq
    groq_api_key: str
    groq_model: str = "llama-3.1-8b-instant"

    # Google Gemini (Embeddings)
    gemini_api_key: str
    gemini_embedding_model: str = "models/text_embeddings-004"

    # Upstash Redis
    upstash_redis_url: str
    upstash_redis_token: str

    # App
    app_name: str = "LoreDex"
    debug: bool = False
    max_upload_size_mb: int = 20


settings = Settings()

    
    