import os
import base64
import hashlib
from pathlib import Path
from datetime import datetime, timedelta, timezone
from typing import Any

import bcrypt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent.parent.parent / ".env")

from app.database import get_connection


SECRET_KEY = os.getenv("JWT_SECRET_KEY", "change-this-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def _normalize_password(password: str) -> bytes:
    digest = hashlib.sha256(password.encode("utf-8")).digest()
    return base64.b64encode(digest)


def hash_password(password: str) -> str:
    normalized_password = _normalize_password(password)
    return bcrypt.hashpw(normalized_password, bcrypt.gensalt()).decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        normalized_password = _normalize_password(plain_password)
        return bcrypt.checkpw(
            normalized_password,
            hashed_password.encode("utf-8"),
        )
    except ValueError:
        return False
    except TypeError:
        return False


def create_access_token(
    data: dict[str, Any],
    expires_delta: timedelta | None = None,
) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def get_user_by_email(email: str) -> dict[str, Any] | None:
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT id, email, hashed_password, created_at
                FROM users
                WHERE email = %s
                """,
                (email.lower(),),
            )
            row = cursor.fetchone()

    return row if row else None


def get_user_by_id(user_id: int) -> dict[str, Any] | None:
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT id, email, hashed_password, created_at
                FROM users
                WHERE id = %s
                """,
                (user_id,),
            )
            row = cursor.fetchone()

    return row if row else None


def create_user(email: str, hashed_password: str) -> dict[str, Any]:
    created_at = datetime.now(timezone.utc).isoformat(timespec="seconds")

    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO users (email, hashed_password, created_at)
                VALUES (%s, %s, %s)
                RETURNING id
                """,
                (email.lower(), hashed_password, created_at),
            )
            user_id = cursor.fetchone()["id"]
        connection.commit()

    return {
        "id": user_id,
        "email": email.lower(),
        "hashed_password": hashed_password,
        "created_at": created_at,
    }


def authenticate_user(email: str, password: str) -> dict[str, Any] | None:
    user = get_user_by_email(email)
    if not user:
        return None

    if not verify_password(password, user["hashed_password"]):
        return None

    return user


async def get_current_user(token: str = Depends(oauth2_scheme)) -> dict[str, Any]:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        user = get_user_by_id(int(user_id))
    except (JWTError, ValueError):
        raise credentials_exception from None

    if not user:
        raise credentials_exception

    return user
