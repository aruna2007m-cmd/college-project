from ai_client import generate_text


def generate_study_schedule(
    subjects: str,
    study_hours: str,
    exam_date: str,
    important_topics: str
) -> str:

    prompt = f"""
You are EduGenie, a personal AI study assistant.

Create a practical study schedule for a student.

Student information:
Subjects: {subjects}
Available study time: {study_hours}
Exam date: {exam_date}
Important topics: {important_topics}

Requirements:
1. Create a clear daily study schedule.
2. Divide the available time properly between subjects.
3. Include short breaks.
4. Include revision time.
5. Include practice/problem-solving time.
6. Give extra attention to important or difficult topics.
7. Keep the plan realistic for a student.
8. Show the schedule in a simple table.
9. Also give a few study tips at the end.

Return only the study schedule and tips.
"""

    return generate_text(
        prompt,
        system_instruction=(
            "You are a helpful personal study planner. "
            "Create simple, realistic and student-friendly study schedules."
        )
    )