import json
import os
import re

from fastapi import APIRouter, HTTPException
from langchain_groq import ChatGroq
from pydantic import BaseModel, Field

router = APIRouter()


def get_model():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        return None
    return ChatGroq(
    groq_api_key=api_key,
    model_name="llama3-8b-8192",
    temperature=0.7,
    )


class QuizRequest(BaseModel):
    topic: str = Field(..., min_length=2, max_length=200)
    num_questions: int = Field(default=5, ge=1, le=10)


@router.get("/")
def quiz_home():
    return {"message": "Quiz API is working. Use POST /quiz/generate"}


@router.post("/generate")
def generate_quiz(request: QuizRequest):
    model = get_model()
    if model is None:
        raise HTTPException(
            status_code=503,
            detail="GROQ_API_KEY missing. Add it to your .env file.",
        )

    prompt = f"""You are a quiz generator. Create exactly {request.num_questions} multiple-choice questions on the topic: "{request.topic}".

Return ONLY a valid JSON array (no markdown, no explanation) in this format:
[
  {{
    "question": "Question text here?",
    "options": ["Option A", "Option B", "Option C", "Option D"],
    "answer": 0
  }}
]

Rules:
- "answer" must be the 0-based index of the correct option (0 to 3).
- Questions should be clear and educational.
- All options must be plausible.
"""

    try:
        response = model.invoke(prompt)
        raw = response.content.strip()

        # Strip markdown code fences if model adds them
        raw = re.sub(r"^```(?:json)?\s*", "", raw)
        raw = re.sub(r"\s*```$", "", raw)

        questions = json.loads(raw)
        if not isinstance(questions, list) or len(questions) == 0:
            raise ValueError("Invalid quiz format")

        cleaned = []
        for q in questions[: request.num_questions]:
            options = q.get("options", [])
            answer = int(q.get("answer", 0))
            if len(options) < 2:
                continue
            answer = max(0, min(answer, len(options) - 1))
            cleaned.append(
                {
                    "question": str(q.get("question", "")).strip(),
                    "options": [str(o) for o in options],
                    "answer": answer,
                }
            )

        if not cleaned:
            raise ValueError("No valid questions generated")

        return {"topic": request.topic, "questions": cleaned}

    except json.JSONDecodeError:
        raise HTTPException(
            status_code=502,
            detail="AI ne valid JSON return nahi kiya. Dubara try karo.",
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
