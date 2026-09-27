from ai_client import generate_text


def get_learning_recommendations(
    topic: str
) -> str:

    prompt = f"""
Create a personalized learning
path for:

{topic}

Organize it from beginner
to advanced.

Include:

1. Prerequisites
2. Beginner topics
3. Intermediate topics
4. Advanced topics
5. Suggested timeline
6. Practice exercises
7. Mini projects
8. Final project
9. Recommended resource types
10. Revision strategy

Make the plan realistic
for a student.

Do not invent specific URLs.
"""


    return generate_text(

        prompt,

        system_instruction="""
You are EduGenie,
a personalized learning-path designer.

Create structured,
practical learning plans.

Use simple language.
"""
    )