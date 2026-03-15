from fastapi import APIRouter
from pydantic import BaseModel
from app.services.negotiation_service import negotiate
from typing import Optional

router = APIRouter(prefix="/negotiation", tags=["Negotiation"])


class NegotiationRequest(BaseModel):
    load_rate: float
    carrier_offer: float
    round_number: int


class NegotiationResponse(BaseModel):
    decision: str
    final_rate: Optional[float] = None
    counter_rate: Optional[float] = None
    reason: Optional[str] = None


@router.post("/", response_model=NegotiationResponse)
def negotiate_rate(request: NegotiationRequest):

    result = negotiate(request.load_rate, request.carrier_offer, request.round_number)
    return result
