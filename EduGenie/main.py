from study_schedule import generate_study_schedule
from  fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field
from qna import answer_question
from explanation_module import explain_concept
from quiz_module import generate_quiz, QuizResponse
from summary_module import summarize_text
from learning_path import get_learning_recommendations


app = FastAPI(
    title="EduGenie",
    description="Google Gemini Powered Learning Assistant",
    version="1.0.0"
)


# -----------------------------
# Static files and templates
# -----------------------------

app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)

templates = Jinja2Templates(
    directory="templates"
)


# -----------------------------
# Request Models
# -----------------------------

class QuestionRequest(BaseModel):
    question: str = Field(                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              
        ...,
        min_length=1,
        max_length=10000
    )


class TextRequest(BaseModel):
    text: str = Field(
        ...,
        min_length=1,
        max_length=30000
    )
class StudyScheduleRequest(BaseModel):
    subjects: str
    study_hours: str
    exam_date: str
    important_topics: str

# -----------------------------
# Home Page
# -----------------------------

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "title": "EduGenie"
        }
    )

# -----------------------------
# Health Check
# -----------------------------

@app.get("/health")
async def health():

    return {
        "status": "ok",
        "application": "EduGenie"
    }


# -----------------------------
# Q&A
# -----------------------------

# -----------------------------
# Q&A
# -----------------------------

@app.post("/qa")
async def qa(payload: QuestionRequest):

    try:

        answer = answer_question(
            payload.question
        )

        return {
            "answer": answer
        }

    except Exception as e:

        print("QA ERROR:", repr(e))

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

# -----------------------------
# Explanation
# -----------------------------

@app.post("/explain")
async def explain(payload: TextRequest):

    try:

        explanation = explain_concept(
            payload.text
        )

        return {
            "explanation": explanation
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# -----------------------------
# Quiz
# -----------------------------

@app.post(
    "/quiz",
    response_model=QuizResponse
)
async def quiz(payload: TextRequest):

    try:

        quiz_result = generate_quiz(
            payload.text
        )

        return quiz_result

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# -----------------------------
# Summarization
# -----------------------------

@app.post("/summarize")
async def summarize(payload: TextRequest):

    try:

        summary = summarize_text(
            payload.text
        )

        return {
            "summary": summary
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# -----------------------------
# Learning Path
# -----------------------------

@app.post("/learn/recommendations")
async def learning_recommendations(
    payload: TextRequest
):

    try:

        learning_path = (
            get_learning_recommendations(
                payload.text
            )
        )

        return {
            "learning_path": learning_path
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
    
@app.post("/study/schedule")
async def study_schedule(request: StudyScheduleRequest):

    try:

        schedule = generate_study_schedule(
            subjects=request.subjects,
            study_hours=request.study_hours,
            exam_date=request.exam_date,
            important_topics=request.important_topics
        )

        return {
            "schedule": schedule
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )