from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]
APP_DIR = ROOT_DIR / "app"
DATA_DIR = APP_DIR / "data"
REFERENTIAL_DIR = DATA_DIR / "referential"
CACHE_DIR = DATA_DIR / "cache"
USER_RESPONSES_DIR = DATA_DIR / "user_responses"

MODEL_NAME = "all-MiniLM-L6-v2"
SIMILARITY_TOP_K = 3
COVERAGE_THRESHOLD = 0.35
