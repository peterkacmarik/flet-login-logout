from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from enum import Enum
# import datetime


class UserRole(Enum):
    ADMIN = "admin"
    USER = "user"
    MODERATOR = "moderator"


class UserBase(BaseModel):
    email: EmailStr = Field(description="User's email address")
    role: Optional[UserRole] = Field(
        default=UserRole.USER,
        description="User's role in the system"
    )
    is_active: Optional[bool] = Field(
        default=True,
        description="Whether the user account is active"
    )
    is_admin: Optional[bool] = Field(
        default=False,
        description="Whether the user has admin privileges"
    )
    is_verified: Optional[bool] = Field(
        default=False,
        description="Whether the user's email is verified"
    )
    
    class Config:
        from_attributes = True
        validate_assignment = True
        json_encoders = {
            datetime: lambda dt: dt.isoformat()
        }


class UserLogin(BaseModel):
    email: EmailStr = Field(description="User's email address")
    password: str = Field(
        min_length=8,
        max_length=100,
        description="User's password"
    )
    jwt_token: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "strongpassword123"
            }
        }
    

class UserCreate(UserBase):
    password: str = Field(
        min_length=8,
        max_length=100,
        description="Password must be between 8 and 100 characters"
    )
    created_at: Optional[datetime] = Field(
        default_factory=datetime.now
    )


class UserUpdate(UserBase):
    password: Optional[str] = Field(
        None,
        min_length=8,
        max_length=100,
        description="Password must be between 8 and 100 characters"
    )
    updated_at: Optional[datetime] = Field(default_factory=datetime.now)


class UserInDBBase(UserBase):
    id: int = Field(description="Unique user identifier")
    created_at: Optional[datetime] = Field(
        default_factory=datetime.now,
        description="Timestamp of user creation"
    )
    last_login: Optional[datetime] = None  # Možno by ste chceli sledovať posledné prihlásenie
    
    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda dt: dt.isoformat()
        }


class User(UserInDBBase):
    pass


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    role: UserRole
    is_active: bool
    is_verified: bool
    created_at: datetime
    
    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda dt: dt.isoformat()
        }


class LoginResponse(BaseModel):
    message: str
    jwt_token: str