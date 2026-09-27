from functools import lru_cache

from google import genai
from google.genai import types

from config import (
    GEMINI_API_KEY,
    GEMINI_MODEL,
)


class AIConfigurationError(RuntimeError):
    pass


# -----------------------------
# Gemini Client
# -----------------------------

@lru_cache(maxsize=1)
def get_client():
    if not GEMINI_API_KEY:
        raise AIConfigurationError(
            "GEMINI_API_KEY is not configured. "
            "Please create a .env file and add your Gemini API key."
        )

    return genai.Client(
        api_key=GEMINI_API_KEY
    )


# -----------------------------
# Normal Text Generation
# -----------------------------

def generate_text(
    prompt: str,
    system_instruction: str | None = None,
) -> str:

    client = get_client()

    config = types.GenerateContentConfig(
        system_instruction=system_instruction,
        max_output_tokens=2048,
    )

    try:
        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt,
            config=config,
        )

        text = getattr(response, "text", None)

        if not text:
            raise RuntimeError(
                "Gemini returned an empty response."
            )

        return text.strip()

    except Exception as e:
        error_text = str(e)

        if "429" in error_text or "RESOURCE_EXHAUSTED" in error_text:
            raise RuntimeError(
                "Gemini quota exceeded. Please wait for the quota "
                "to reset or enable billing."
            ) from e

        if "503" in error_text or "UNAVAILABLE" in error_text:
            raise RuntimeError(
                "Gemini is temporarily unavailable. "
                "Please try again later."
            ) from e

        raise


# -----------------------------
# Structured JSON Generation
# -----------------------------

def generate_json(
    prompt: str,
    schema_model,
):

    client = get_client()

    config = types.GenerateContentConfig(
        max_output_tokens=4096,
        response_mime_type="application/json",
        response_schema=schema_model,
        system_instruction=(
            "Return only valid data matching "
            "the supplied JSON schema."
        ),
    )

    try:
        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt,
            config=config,
        )

        text = getattr(response, "text", None)

        if not text:
            raise RuntimeError(
                "Gemini returned an empty response."
            )

        return schema_model.model_validate_json(text)

    except Exception as e:
        error_text = str(e)

        if "429" in error_text or "RESOURCE_EXHAUSTED" in error_text:
            raise RuntimeError(
                "Gemini quota exceeded. Please wait for the quota "
                "to reset or enable billing."
            ) from e

        if "503" in error_text or "UNAVAILABLE" in error_text:
            raise RuntimeError(
                "Gemini is temporarily unavailable. "
                "Please try again later."
            ) from e

        raise