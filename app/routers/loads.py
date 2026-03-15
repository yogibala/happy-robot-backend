from fastapi import APIRouter, Query
import json
from pathlib import Path
from typing import List, Optional

router = APIRouter(prefix="/loads", tags=["Loads"])

# Load data once at startup
data_path = Path(__file__).parent.parent / "data" / "loads.json"
with open(data_path) as f:
    loads_db = json.load(f)


@router.get("/search")
def search_loads( # type: ignore
    origin: Optional[str] = Query(None), 
    destination: Optional[str] = Query(None)
):
    results = []
    for load in loads_db:
        # Check if the search terms are contained within the load fields
        match_o = not origin or origin.lower() in load["origin"].lower()
        match_d = not destination or destination.lower() in load["destination"].lower()

        if match_o and match_d:
            results.append(load)

    return results if results else {"message": "No matching loads found."} # type: ignore

@router.get("/{load_id}")
def get_load(load_id: str):
    for load in loads_db:
        if load["load_id"] == load_id:
            return load
    return {"error": "Load not found"}
