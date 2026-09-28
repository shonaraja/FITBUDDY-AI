import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{BASE_DIR / 'fitbuddy.db'}")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()

# These can be changed in .env without editing Python code.
# The project documentation names Gemini Pro/Flash; current Gemini API model
# names change over time, so the defaults are configurable.
GEMINI_WORKOUT_MODEL = os.getenv("GEMINI_WORKOUT_MODEL", "gemini-3.8-flash")
GEMINI_TIP_MODEL = os.getenv("GEMINI_TIP_MODEL", "gemini-3.8-flash")

APP_NAME = "FitBuddy"
AI_ENABLED = bool(GEMINI_API_KEY)
