from ai_client import generate_text


SYSTEM_PROMPT = """
You are EduGenie, an educational AI assistant.

Your job is to answer student questions accurately
and in simple language.

Rules:

1. Give clear answers.
2. Explain difficult terms.
3. Use examples when helpful.
4. Avoid unnecessary technical language.
5. Do not invent facts.
6. If the question is ambiguous, clearly state your assumption.
7. Keep answers suitable for students.
"""


def answer_question(
    question: str
) -> str:

    prompt = f"""
Answer the following student question:

{question}

Give a clear and educational answer.
"""

    return generate_text(
        prompt,
        system_instruction=SYSTEM_PROMPT
    )
