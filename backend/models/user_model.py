# from datetime import datetime
from typing import Optional
from passlib.context import CryptContext
from enum import Enum
from datetime import datetime

from sqlalchemy import Boolean, Column, Integer, String, DateTime, Enum as SQLAlchemyEnum
from sqlalchemy.orm import declarative_base

from backend.schemas.user_schema import UserRole


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
Base = declarative_base()


class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    
    # Role a oprávnenia
    role = Column(SQLAlchemyEnum(UserRole), default=UserRole.USER)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    is_verified = Column(Boolean, default=False)
    
    # Časové značky
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    last_login = Column(DateTime, nullable=True)
    
    def __repr__(self):
        return f"<User {self.email}>"
    
    @property
    def is_authenticated(self) -> bool:
        return True if self.is_active else False
    
    @property
    def is_anonymous(self) -> bool:
        return False
    
    def get_id(self) -> str:
        return str(self.id)
    
    def set_password(self, password: str):
        """Zahashuje a nastaví heslo používateľa"""
        self.hashed_password = pwd_context.hash(password)
    
    def verify_password(self, plain_password: str) -> bool:
        """Overí, či zadané heslo zodpovedá zahashovanému heslu"""
        return pwd_context.verify(plain_password, self.hashed_password)
    
    def set_role(self, role: str):
        """Nastaví používateľskú rolu po normalizácii na veľké písmená"""
        self.role = UserRole[role.upper()]  # Normalizácia na veľké písmená
    
    def update(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.updated_at = datetime.utcnow()
    
    @classmethod
    async def get_by_email(cls, db_session, email: str):
        return await db_session.query(cls).filter(cls.email == email).first()
    
    @classmethod
    async def get_by_id(cls, db_session, id: int):
        return await db_session.query(cls).filter(cls.id == id).first()
    
    @classmethod
    async def create(cls, db_session, **kwargs):
        obj = cls(**kwargs)
        db_session.add(obj)
        await db_session.flush()
        return obj
    
    async def save(self, db_session):
        if not self.id:
            db_session.add(self)
        self.updated_at = datetime.utcnow()
        await db_session.flush()
        return self
    
    async def delete(self, db_session):
        await db_session.delete(self)
        await db_session.flush()

    @classmethod
    async def authenticate(cls, db_session, email: str, password: str):
        """Autentifikuje používateľa na základe emailu a hesla"""
        user = await cls.get_by_email(db_session, email)
        if not user:
            return None
        if not user.verify_password(password):
            return None
        return user
    
    async def update_last_login(self, db_session):
        """Aktualizuje čas posledného prihlásenia"""
        self.last_login = datetime.utcnow()
        await self.save(db_session)
        
        