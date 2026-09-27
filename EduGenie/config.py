import os

from dotenv import load_dotenv


# Load .env file
load_dotenv()


# -----------------------------
# Application
# -----------------------------

APP_NAME = "EduGenie"


# -----------------------------
# Gemini Configuration
# -----------------------------

GEMINI_API_KEY = os.getenv(
    "GEMINI_API_KEY",
    ""
).strip()

GEMINI_MODEL = os.getenv(
    "GEMINI_MODEL",
    "gemini-3.6-flash"
)



# -----------------------------
# Local Explanation Model
# -----------------------------

LOCAL_EXPLAINER = os.getenv(
    "LOCAL_EXPLAINER",
    "false"
).lower() == "true"


LOCAL_MODEL = os.getenv(
    "LOCAL_MODEL",
    "MBZUAI/LaMini-Flan-T5-783M"
)