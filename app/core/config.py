from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_env: str = "development"
    log_level: str = "INFO"

    groq_api_key: str | None = None
    groq_model: str = "openai/gpt-oss-20b"
    groq_temperature: float = 0.1

    tavily_api_key: str | None = None
    tavily_max_results: int = 5

    embedding_model: str = "BAAI/bge-small-en-v1.5"
    chroma_dir: str = "storage/chroma"
    upload_dir: str = "data/uploads"
    collection_name: str = "research_documents"

    chunk_size: int = 900
    chunk_overlap: int = 150
    top_k: int = 5
    min_relevance: float = 0.25

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    def ensure_dirs(self) -> None:
        Path(self.chroma_dir).mkdir(parents=True, exist_ok=True)
        Path(self.upload_dir).mkdir(parents=True, exist_ok=True)


@lru_cache
def get_settings() -> Settings:
    settings = Settings()
    settings.ensure_dirs()
    return settings
