# auth.py
# Handles password hashing and JWT (JSON Web Token) creation/verification.
# This is your "Auth" deliverable.

from datetime import datetime, timedelta
from passlib.context import CryptContext
import jwt

# --- Config ---
# In a real app this secret would come from an environment variable.
# For a 1-week student prototype, a hardcoded constant is fine — just don't
# reuse this in anything real.
SECRET_KEY = "sprint-project-secret-change-me"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 90

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(plain_password: str) -> str:
    """Turn a plain password into a secure hash before saving it to the DB."""
    return pwd_context.hash(plain_password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Check a login attempt's password against the stored hash."""
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(user_id: int, role: str) -> str:
    """
    Create a JWT that encodes who this user is and what role they have.
    The frontend will send this token back on every request; your endpoints
    check it to decide what the user is allowed to do.
    """
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {
        "sub": str(user_id),   # "subject" — who this token belongs to
        "role": role,
        "exp": expire,
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token


def decode_access_token(token: str) -> dict:
    """
    Reverse of create_access_token — reads a token and returns the payload.
    Raises an exception if the token is invalid or expired (FastAPI will
    turn that into a 401 error automatically, see main.py).
    """
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    return payload
