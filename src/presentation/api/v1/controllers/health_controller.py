from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
import jwt


router = APIRouter(prefix="/health", tags=["health"])


# security = HTTPBearer()

# # Your JWT secret key and algorithm
# JWT_SECRET_KEY = "your-secret-key"
# JWT_ALGORITHM = "HS256"

# async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
#     """
#     Validate JWT token and return user information.
#     Only used for endpoints that need authentication.
#     """
#     try:
#         token = credentials.credentials
#         payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
#         user_id = payload.get("user_id")
        
#         if user_id is None:
#             raise HTTPException(
#                 status_code=status.HTTP_401_UNAUTHORIZED,
#                 detail="Invalid authentication credentials",
#                 headers={"WWW-Authenticate": "Bearer"},
#             )
        
#         return {"user_id": user_id, **payload}
    
#     except jwt.PyJWTError:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid authentication credentials",
#             headers={"WWW-Authenticate": "Bearer"},
#         )

@router.get("/", status_code=status.HTTP_200_OK)
async def health_check():
    return {"status": "ok", "message": "Service is running"}
