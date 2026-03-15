from fastapi import APIRouter
from pydantic import BaseModel

from app.database import conn
from app.services.call_analysis_service import analyze_call

router = APIRouter(
    prefix="/call-analysis",
    tags=["Call Analysis"]
)


class CallTranscript(BaseModel):
    transcript: str


@router.post("/")
def analyze_call_transcript(request: CallTranscript):

    # run LLM extraction
    result = analyze_call(request.transcript)

    # store result in database
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO calls (mc_number, load_id, final_rate, outcome, sentiment)
        VALUES (?, ?, ?, ?, ?)
    """, (
        result.get("mc_number"),
        result.get("load_id"),
        result.get("final_rate"),
        result.get("outcome"),
        result.get("sentiment")
    ))

    conn.commit()

    return result