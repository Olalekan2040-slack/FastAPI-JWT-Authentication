#The function is to check wheter the request is authorized or not [ Verification of the protected route]

from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from .jwt_handler import decodeJWT

class jwtBrearer(HTTPBearer):
    def __innit__(self, auto_Error : bool = True):
        super(jwtBrearer, self).__init__(auto_error=auto_Error)


    async def __call__(self, request : Request):
        credentials : HTTPAuthorizationCredentials = await super(jwtBrearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, details="Invalid or Expired Token")
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, details="Invalid or Expired Token")
        


    def verify_jwt(self,jwtoken : str):
        isTokenValid : bool = False
        payload = decodeJWT(jwtoken)
        if payload:
            isTokenValid = True
        return isTokenValid