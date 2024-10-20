# Autentifikačné trasy (login, reset hesla)
from fastapi import APIRouter, Depends, HTTPException, Response, Request, FastAPI
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.database import get_db
from backend.core.secutity import create_jwt_token, verify_jwt_token
from backend.schemas.user_schema import UserCreate, UserLogin, UserResponse, User, LoginResponse
# from models.user_model import UserModel
from backend.database.crud_db import authenticate_user, create_user, get_user_by_email

from backend.core.config import Config
import jwt
import datetime
from datetime import timedelta
from pydantic import BaseModel


auth_router = APIRouter()


# Registrácia používateľa
@auth_router.post("/register")
async def register_user(user: UserCreate, db: AsyncSession = Depends(get_db)) -> User:
    db_user = await get_user_by_email(db=db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user = await create_user(db=db, user=user)
    return new_user
    

# Prihlasenie používateľa
@auth_router.post("/login", response_model=LoginResponse)
async def login(response: Response, user: UserLogin, db: AsyncSession = Depends(get_db)) -> dict:
    auth_user = await authenticate_user(db=db, email=user.email, password=user.password)
    
    if auth_user is None:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    # access_token: str = create_jwt_token({"email": auth_user.email})
    access_token: str = create_jwt_token({
        "email": auth_user.email, 
        "exp": datetime.datetime.now() + timedelta(minutes=Config.ACCESS_TOKEN_EXPIRE_MINUTES)
    })
    
    response.set_cookie(
        key="jwt_token", 
        value=access_token, 
        httponly=True, 
        max_age=Config.ACCESS_TOKEN_EXPIRE_MINUTES * 60,  # Trvanie cookie
        samesite="strict", #"lax", # Zabraňuje CSRF útokom
        secure=False, # Nastav na True, ak používaš HTTPS
        # domain=Config.DOMAIN
    )

    # return auth_user, {"access_token": access_token}
    return LoginResponse(
        message="Logged in successfully!",
        jwt_token =access_token,
    )


# Logout endpoint - odstranenie JWT tokenu z cookie
@auth_router.get("/logout")
async def logout(response: Response):
    response.delete_cookie("jwt_token")
    return {"message": "Logout successful"}


# Chraneny endpoint - pouzitie JWT tokenu z cookie
@auth_router.get("/verify-token")
async def verify_token(request: Request) -> dict:
    token: str = request.cookies.get("jwt_token")

    if token is None:
        raise HTTPException(status_code=403, detail=f"Not authenticated or token not found: {token}")

    try:
        decode_token: dict = verify_jwt_token(token)
        if decode_token is None:
            raise HTTPException(status_code=403, detail="Invalid token")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=403, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=403, detail="Invalid token")
    
    return {
        "message": f"Welcome to protected route: {decode_token.get('email')}",
        "token": token,
        "decode_token": decode_token
    }



# @auth_router.get("/verify-token")
# async def verify_token(request: Request) -> dict:
#     token: str = request.cookies.get("jwt_token")
#     if not token:
#         raise HTTPException(status_code=401, detail="No token provided")
#     try:
#         decode_token: dict = verify_jwt_token(token)
#         return {"valid": True, "email": decode_token.get("email")}
#     except:
#         return {"valid": False}