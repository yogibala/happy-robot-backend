from typing import Dict, Any
import requests
from app.config import FMCSA_API_KEY

BASE_URL = "https://api.fmcsa.dot.gov/safety/v1/carrier/docket-number"

# Explicitly defining the return type resolves the "Unknown" error
def verify_carrier(mc_number: str) -> Dict[str, Any]:
    url = f"{BASE_URL}/{mc_number}?api_key={FMCSA_API_KEY}"
    print(f"DEBUG: Verifying carrier with MC number: {FMCSA_API_KEY}")
    try:
        response = requests.get(url, timeout=10)
        
        # Logging for your verification
        print(f"DEBUG: FMCSA Request URL: {url}")
        print(f"DEBUG: FMCSA Status Code: {response.status_code}")

        if response.status_code != 200:
            return {"verified": False, "error": f"API returned {response.status_code}"}

        data = response.json()

        if "content" not in data or not data["content"]:
            print("DEBUG: No carrier content found in response")
            return {"verified": False}

        carrier = data["content"][0]
        
        return {
            "verified": True,
            "carrier_name": carrier.get("legalName"),
            "status": carrier.get("carrierOperation")
        }
    except Exception as e:
        print(f"DEBUG: Connection error: {str(e)}")
        return {"verified": False, "error": "Connection failed"}