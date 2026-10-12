import os
from pathlib import Path

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parent.parent

load_dotenv(PROJECT_ROOT / ".env")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

DATABASE_PATH = PROJECT_ROOT / "data" / "onyx_fit.db"
KNOWLEDGE_PATH = PROJECT_ROOT / "data" / "knowledge"
VECTORSTORE_PATH = PROJECT_ROOT / "data" / "vectorstore"

SCHEMA_PATH = PROJECT_ROOT / 'schema.json'
