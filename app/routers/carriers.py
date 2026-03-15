from fastapi import APIRouter, Body
from app.services.fmcsa_service import verify_carrier

router = APIRouter(prefix="/carriers", tags=["Carriers"])

@router.post("/verify")
def verify(mc_number: str = Body(..., embed=True)):
    """
    Accepts mc_number from a JSON body: {"mc_number": "123456"}
    """
    # Optional: Add numeric-only validation here before calling the service
    result = verify_carrier(mc_number)
    return result