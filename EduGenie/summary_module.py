from ai_client import generate_text


def summarize_text(
    text: str
) -> str:

    prompt = f"""
Summarize the following educational
content.

Requirements:

- Keep the important information.
- Remove repetition.
- Use simple language.
- Make it useful for revision.
- Do not add unsupported information.
- Use bullet points where useful.

Content:

{text}
"""


    return generate_text(

        prompt,

        system_instruction="""
You are EduGenie,
an educational summarization assistant.

Your summaries should be concise,
clear and useful for students.
"""
    )