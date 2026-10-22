"""Configuration. Everything comes from environment variables with safe defaults."""
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent


def _flag(name: str, default: str = "0") -> bool:
    return os.environ.get(name, default).strip().lower() in {"1", "true", "yes", "on"}


class Config:
    CONTENT_DIR = Path(os.environ.get("CONTENT_DIR", BASE_DIR / "content"))
    # In production only questions with "reviewed": true are served.
    REQUIRE_REVIEWED = _flag("REQUIRE_REVIEWED")
    TRUST_PROXY = _flag("TRUST_PROXY")
    # Requests per minute per IP for POST endpoints (quiz grading, answer checks).
    RATE_LIMIT_PER_MIN = int(os.environ.get("RATE_LIMIT", "60"))
    # Optional overrides; defaults come from content/syllabus.json "exam_simulation".
    EXAM_QUESTIONS = os.environ.get("EXAM_QUESTIONS")
    EXAM_MINUTES = os.environ.get("EXAM_MINUTES")
    MAX_CONTENT_LENGTH = 64 * 1024  # form/JSON bodies are tiny; reject anything bigger
