import os
from functools import lru_cache

from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    openai_api_key: str = Field(..., env="OPENAI_API_KEY")
    model_name: str = Field("gpt-4o-mini", env="MODEL_NAME")
    embedding_model: str = Field("text-embedding-3-small", env="EMBEDDING_MODEL")

    documents_path: str = Field("data/documents", env="DOCUMENTS_PATH")
    faiss_index_path: str = Field("data/faiss_index", env="FAISS_INDEX_PATH")
    top_k: int = Field(5, env="TOP_K")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    return Settings()

