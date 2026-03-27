from fastapi import APIRouter, Depends, HTTPException, Request, status

from app.auth.models import TokenResponse, UserCreate, UserLogin, UserResponse
from app.auth.utils import (
    authenticate_user,
    create_access_token,
    create_user,
    get_current_user,
    get_user_by_email,
    hash_password,
)


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register")
async def register_user(payload: UserCreate) -> dict[str, str]:
    if get_user_by_email(payload.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered.",
        )

    hashed_password = hash_password(payload.password)
    create_user(payload.email, hashed_password)
    return {"message": "User registered successfully."}


@router.post("/login", response_model=TokenResponse)
async def login_user(
    request: Request,
) -> TokenResponse:
    email = ""
    password = ""

    content_type = request.headers.get("content-type", "").lower()
    if "application/json" in content_type:
        payload = UserLogin.model_validate(await request.json())
        email = payload.email
        password = payload.password
    else:
        form_data = await request.form()
        email = str(form_data.get("email") or form_data.get("username") or "").strip()
        password = str(form_data.get("password") or "")

        if not email or not password:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Email and password are required.",
            )

    user = authenticate_user(email, password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = create_access_token({"sub": str(user["id"])})
    return TokenResponse(access_token=token)


@router.get("/me", response_model=UserResponse)
async def read_me(current_user: dict = Depends(get_current_user)) -> UserResponse:
    return UserResponse(
        id=current_user["id"],
        email=current_user["email"],
        created_at=current_user["created_at"],
    )
