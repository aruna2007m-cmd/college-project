from ai_client import generate_text

from config import (
    LOCAL_EXPLAINER,
    LOCAL_MODEL
)


_local_pipeline = None


# -----------------------------
# Load Local Model
# -----------------------------

def get_local_pipeline():

    global _local_pipeline


    if _local_pipeline is None:

        try:

            from transformers import pipeline

        except ImportError:

            raise RuntimeError(
                "Transformers is not installed. "
                "Run: pip install -r requirements.txt"
            )


        _local_pipeline = pipeline(

            "text2text-generation",

            model=LOCAL_MODEL,

            device=-1
        )


    return _local_pipeline


# -----------------------------
# Local Explanation
# -----------------------------

def local_explanation(
    topic: str
) -> str:

    pipeline_model = (
        get_local_pipeline()
    )


    prompt = f"""
Explain the following topic
to a beginner.

Topic:

{topic}

Give:

1. Simple definition
2. How it works
3. Simple example
4. Important point
"""


    result = pipeline_model(

        prompt,

        max_new_tokens=300,

        do_sample=False
    )


    return result[0][
        "generated_text"
    ].strip()


# -----------------------------
# Main Explanation Function
# -----------------------------

def explain_concept(
    topic: str
) -> str:

    if LOCAL_EXPLAINER:

        return local_explanation(
            topic
        )


    prompt = f"""
Explain the following concept
to a beginner:

{topic}

Use this structure:

1. Simple Definition
2. How It Works
3. Easy Example
4. Key Point to Remember
"""


    return generate_text(

        prompt,

        system_instruction="""
You are EduGenie.

Explain difficult educational
concepts in a simple and friendly
way.

Assume the student is a beginner.
Avoid unnecessary jargon.
"""
    )