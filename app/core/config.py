from pathlib import Path


class Settings:
    APP_NAME: str = "Drift-Aware LLMOps Monitoring Pipeline"

    EMBEDDING_MODEL_NAME: str = "all-MiniLM-L6-v2"

    VECTOR_DB_PATH: str = "data/vector_db"
    COLLECTION_NAME: str = "knowledge_base"

    LOG_DIR: Path = Path("logs")
    LOG_FILE: Path = LOG_DIR / "rag_requests.jsonl"

    DEFAULT_TOP_K: int = 3


settings = Settings()