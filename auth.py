import os

from fastapi import HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from starlette.middleware.base import BaseHTTPMiddleware


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Allow OPTIONS requests to pass through without authorization check
        if request.method == "OPTIONS":
            return await call_next(request)

        authorization: str = request.headers.get("Authorization")
        if not authorization:
            raise HTTPException(status_code=401, detail="Unauthorized")
        token = authorization.split(" ")[1]
        AUTH_TOKEN = os.getenv("AUTH_TOKEN")

        # token_auth_scheme = HTTPBearer()
        # http_auth: HTTPAuthorizationCredentials = await token_auth_scheme(request)
        # if http_auth.credentials != AUTH_TOKEN:
        if token != AUTH_TOKEN:
            raise HTTPException(status_code=403, detail="Invalid token")
        response = await call_next(request)
        return response
