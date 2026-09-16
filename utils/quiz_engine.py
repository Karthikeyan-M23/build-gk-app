import json

from utils.openai_client import client


def generate_quiz(
    category,
    difficulty,
    number_of_questions
):

    prompt = f"""
Create a general knowledge multiple-choice quiz.

Category: {category}
Difficulty: {difficulty}
Number of questions: {number_of_questions}

Requirements:

1. Each question must have exactly 4 options.
2. Only one option must be correct.
3. Questions must be factually accurate.
4. Avoid duplicate questions.
5. Provide a short explanation for the correct answer.
6. Keep questions suitable for a general knowledge quiz.

Return ONLY valid JSON.

Use exactly this structure:

{{
    "questions": [
        {{
            "question": "Question text",
            "options": [
                "Option A",
                "Option B",
                "Option C",
                "Option D"
            ],
            "correct_answer": "Option A",
            "explanation": "Short explanation"
        }}
    ]
}}
"""

    response = client.responses.create(
        model="gpt-4o-mini",
        input=prompt
    )

    result = response.output_text

    result = result.replace("```json", "")
    result = result.replace("```", "")
    result = result.strip()

    quiz_data = json.loads(result)

    return quiz_data