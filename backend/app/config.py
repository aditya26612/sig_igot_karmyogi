import os
from pathlib import Path
from typing import List
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parents[1]
load_dotenv(BASE_DIR / ".env")

class Settings:
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    PORT: int = int(os.getenv("PORT", "8000"))
    HOST: str = os.getenv("HOST", "127.0.0.1")
    
    # JWT Settings
    JWT_SECRET: str = os.getenv("JWT_SECRET", "sih26101-karmayogi-super-secure-secret-key-2026-prod")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "1440"))
    
    # Groq Settings
    _raw_groq_keys: str = os.getenv("GROQ_API_KEYS", "")
    GROQ_PRIMARY_MODEL: str = os.getenv("GROQ_PRIMARY_MODEL", "openai/gpt-oss-20b")
    GROQ_FAST_MODEL: str = os.getenv("GROQ_FAST_MODEL", "openai/gpt-oss-20b")

    # ---- RAG / LLM routing ----
    OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434")
    OLLAMA_MODEL: str = os.getenv("OLLAMA_MODEL", "qwen2.5:1.5b")
    RAG_RERANKER_ENABLED: bool = os.getenv("RAG_RERANKER_ENABLED", "1").lower() in ("1", "true", "yes")
    RAG_EMBEDDING_MODEL: str = os.getenv("RAG_EMBEDDING_MODEL", "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
    RAG_RERANKER_MODEL: str = os.getenv("RAG_RERANKER_MODEL", "BAAI/bge-reranker-v2-m3")
    RAG_CHUNK_TARGET_CHARS: int = int(os.getenv("RAG_CHUNK_TARGET_CHARS", "900"))
    RAG_CHUNK_OVERLAP_CHARS: int = int(os.getenv("RAG_CHUNK_OVERLAP_CHARS", "225"))
    GROQ_ASSISTANT_TIMEOUT_S: float = float(os.getenv("GROQ_ASSISTANT_TIMEOUT_S", "8"))
    GROQ_QUIZ_TIMEOUT_S: float = float(os.getenv("GROQ_QUIZ_TIMEOUT_S", "20"))

    # Perceived generation delay: makes AI quiz/assessment generation feel like live synthesis in demos
    AI_PRESENTATION_DELAY_SECONDS: float = float(os.getenv("AI_PRESENTATION_DELAY_SECONDS", "3"))
    
    # Paths
    DATA_DIR: Path = BASE_DIR / "data"
    DB_PATH: Path = DATA_DIR / "demo.sqlite"
    TABLE_ORDER_PATH: Path = DATA_DIR / "table_order.json"
    
    # CORS
    CORS_ORIGINS: List[str] = [
        origin.strip() for origin in os.getenv("CORS_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173").split(",")
        if origin.strip()
    ]
    
    @property
    def groq_keys(self) -> List[str]:
        keys = [k.strip() for k in self._raw_groq_keys.split(",") if k.strip()]
        return keys

settings = Settings()
