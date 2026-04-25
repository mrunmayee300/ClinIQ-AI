from __future__ import annotations

from fastapi import HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt

from utils.config import settings

bearer_scheme = HTTPBearer(auto_error=False)


def require_jwt(credentials: HTTPAuthorizationCredentials = Security(bearer_scheme)) -> dict:
    if not credentials:
        raise HTTPException(status_code=401, detail="Missing authorization token.")
    token = credentials.credentials
    try:
        payload = jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
    except JWTError as exc:
        raise HTTPException(status_code=401, detail="Invalid authorization token.") from exc
    return payload
