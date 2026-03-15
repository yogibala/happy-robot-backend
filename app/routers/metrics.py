from fastapi import APIRouter
from app.database import conn

router = APIRouter(
    prefix="/metrics",
    tags=["Metrics"]
)


@router.get("/")
def get_metrics():

    cursor = conn.cursor()

    total_calls = cursor.execute(
        "SELECT COUNT(*) FROM calls"
    ).fetchone()[0]

    deals_closed = cursor.execute(
        "SELECT COUNT(*) FROM calls WHERE outcome='deal_closed'"
    ).fetchone()[0]

    positive_sentiment = cursor.execute(
        "SELECT COUNT(*) FROM calls WHERE sentiment='positive'"
    ).fetchone()[0]

    avg_rate = cursor.execute(
    "SELECT COALESCE(AVG(final_rate), 0) FROM calls"
    ).fetchone()[0]

    return {
        "total_calls": total_calls,
        "deals_closed": deals_closed,
        "positive_sentiment": positive_sentiment,
        "avg_rate": avg_rate
    }