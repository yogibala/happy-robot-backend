from fastapi import APIRouter
from app.services.fmcsa_service import verify_carrier

router = APIRouter(
    prefix="/carriers",
    tags=["Carriers"]
)


@router.post("/verify")
def verify(mc_number: str):

    result = verify_carrier(mc_number)

    return result