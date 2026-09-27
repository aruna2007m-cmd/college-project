from pydantic import BaseModel, Field

from ai_client import generate_json


# -----------------------------
# Quiz Question
# -----------------------------

class QuizQuestion(BaseModel):

    question: str

    options: list[str] = Field(
        min_length=4,
        max_length=4
    )

    correct_answer: str


# -----------------------------
# Quiz Response
# -----------------------------

class QuizResponse(BaseModel):

    questions: list[
        QuizQuestion
    ] = Field(
        min_length=3,
        max_length=3
    )


# -----------------------------
# Generate Quiz
# -----------------------------

def generate_quiz(
    text: str
) -> QuizResponse:

    prompt = f"""
Create exactly 3 multiple-choice
questions from the educational
content below.

Rules:

1. Create exactly 3 questions.
2. Every question must have exactly
   4 options.
3. Only one option should be correct.
4. correct_answer must exactly match
   one of the options.
5. Questions must be based only on
   the supplied content.
6. Make incorrect options plausible.
7. Cover different important ideas.

Educational content:

{text}
"""


    quiz = generate_json(
        prompt,
        QuizResponse
    )


    # Extra validation
    for question in quiz.questions:

        if (
            question.correct_answer
            not in question.options
        ):

            raise ValueError(
                "Invalid quiz answer returned by Gemini."
            )


    return quiz