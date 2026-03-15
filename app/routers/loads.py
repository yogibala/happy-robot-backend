from fastapi import APIRouter
import json
from pathlib import Path

router = APIRouter(
    prefix="/loads",
    tags=["Loads"]
)

# load data from file
data_path = Path(__file__).parent.parent / "data" / "loads.json"

with open(data_path) as f:
    loads = json.load(f)


@router.get("/")
def get_loads():
    return loads


@router.get("/{load_id}")
def get_load(load_id: str):

    for load in loads:
        if load["load_id"] == load_id:
            return load

    return {"error": "Load not found"}