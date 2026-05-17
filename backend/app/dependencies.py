from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from supabase import create_client, Client

from app.config import settings

# Expect a Bearer Token
bearer_scheme = HTTPBearer()


def get_supabase() -> Client:
    return create_client(settings.supabase_url, settings.supabase_service_role_key)

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme), 
    supabase: Client = Depends(get_supabase),
) -> dict:
    token = credentials.credentials

    try:
        response = supabase.auth.get_user(token)
        return response.user
    except Exception:
        return HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )