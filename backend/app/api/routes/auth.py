from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr
from supabase import Client

from app.dependencies import get_supabase


router = APIRouter(prefix="/auth", tags=["auth"])


# schemas

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class AuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: str


# routes

@router.post("/register", response_model=AuthResponse)
async def register(
    body: RegisterRequest,
    supabase: Client = Depends(get_supabase),
):
    try:
        response = supabase.auth.sign_up({
            "email": body.email,
            "password": body.password,
        })

        if not response.user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                details="Registration failed",
            )

        return AuthResponse(
            access_token=response.session.access_token,
            user_id=str(response.user.id),
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.post("/login", response_model=AuthResponse)
async def login(
    body: LoginRequest,
    supabase: Client = Depends(get_supabase),
):
    try:
        response = supabase.auth.sign_in_with_password({
            "email": body.email,
            "password": body.password,
        })

        if not response.user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
            )

        return AuthResponse(
            access_token=response.session.access_token,
            user_id=str(response.user.id),
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
        )