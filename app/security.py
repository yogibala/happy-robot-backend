from fastapi import Security, HTTPException, status
from fastapi.security.api_key import APIKeyHeader
from app.config import APP_API_KEY # Ensure this is in your config.py

API_KEY_NAME = "X-API-Key"
# auto_error=False allows us to handle the error manually for a cleaner response
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

async def get_api_key(api_key_header: str = Security(api_key_header)):
    if api_key_header == APP_API_KEY:
        return api_key_header
    else:
        # If the key is missing or wrong, the backend stops the request here
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Unauthorized: Invalid or missing API Key",
        )