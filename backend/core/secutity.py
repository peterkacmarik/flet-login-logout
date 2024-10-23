# Tokeny, JWT, hashing hesiel
import jwt
from datetime import timedelta
from passlib.hash import argon2
from fastapi import FastAPI, Depends, HTTPException
import datetime
# from backend.core.config import Config
from dotenv import load_dotenv
import os

load_dotenv()  # Načítanie .env súboru

ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
SECRET_KEY = os.getenv("SECRET_KEY")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")

def generate_password_hash(password: str) -> str:
    return argon2.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    return argon2.verify(password, password_hash)


def create_jwt_token(data: dict):
    to_encode: dict = data.copy()
    expire: datetime = datetime.datetime.now() + timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    token: str = jwt.encode(to_encode, SECRET_KEY, algorithm=JWT_ALGORITHM)
    return token


def verify_jwt_token(token: str):
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[JWT_ALGORITHM])
        return decoded_token if decoded_token["exp"] >= datetime.datetime.now().timestamp() else None
    except jwt.PyJWTError:
        return None
    
    
# response = [
#   {
#     "hashed_password": "$argon2id$v=19$m=65536,t=3,p=4$wTinFCKkdO79f+8do5QyRg$Jy1SIIVSjLA1/RjJOYLMSwskWcE2unwrTZVrq6WDG1k",
#     "email": "user@example.com",
#     "id": 1,
#     "uuid": "47bc08a8-eeb1-426a-a5e0-aca31359b95f",
#     "is_active": True,
#     "is_verified": False,
#     "update_at": None,
#     "role": "user",
#     "is_admin": False,
#     "created_at": "2024-10-06T17:18:58.804272"
#   },
#   {
#     "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InVzZXJAZXhhbXBsZS5jb20iLCJleHAiOjE3Mjg0MDkxMzR9.2bxWxIjiw749kHD8Age2xSisOKMtXmjs6yVXh68AqUM"
#   }
# ]

# print(response[1].get("access_token"))