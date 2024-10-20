from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from backend.models.user_model import UserModel
from backend.schemas.user_schema import UserCreate, UserUpdate
from backend.core.secutity import generate_password_hash, verify_password

from datetime import date
from typing import Optional
import datetime


async def create_user(db: AsyncSession, user: UserCreate):
    hashed_password = generate_password_hash(user.password)
    db_user = UserModel(
        email=user.email,
        hashed_password=hashed_password,
        role=user.role,
        is_active=user.is_active,
        is_admin=user.is_admin,
        is_verified=user.is_verified,
        created_at=user.created_at,
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


async def authenticate_user(db: AsyncSession, email: str, password: str) -> Optional[UserModel]:
    user = await get_user_by_email(db, email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


async def get_user_by_email(db: AsyncSession, email: str) -> Optional[UserModel]:
    result = await db.execute(select(UserModel).filter(UserModel.email == email))
    return result.scalars().first()


async def get_user_id(db: AsyncSession, user_id: int) -> Optional[UserModel]:
    result = await db.execute(select(UserModel).filter(UserModel.id == user_id))
    return result.scalars().first()


async def get_users(db: AsyncSession, skip: int = 0, limit: int = 10):
    result = await db.execute(select(UserModel).offset(skip).limit(limit))
    return result.scalars().all()


async def update_user(db: AsyncSession, db_user: UserModel, user_update: UserUpdate) -> UserModel:
    if user_update.email:
        db_user.email = user_update.email
    if user_update.password:
        hashed_password = generate_password_hash(user_update.password)
        db_user.hashed_password = hashed_password  # Nezabudni hashovať heslo
    db_user.is_active = user_update.is_active
    db_user.is_admin = user_update.is_admin
    db_user.update_at = datetime.now()

    await db.commit()
    await db.refresh(db_user)
    return db_user


async def delete_user(db: AsyncSession, user_id: int) -> Optional[UserModel]:
    user = await db.execute(select(UserModel).filter(UserModel.id == user_id))
    user = user.scalars().first()
    if user:
        db.delete(user)
        await db.commit()
        return user
    return None

