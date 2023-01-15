from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credential: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credential:
            if not credential.scheme == "Bearer":
                raise HTTPException(401, "Authorization failed")
            return credential.credentials
        else:
            raise HTTPException(401, "Authorization failed")