from sqlalchemy import Boolean, Column, Integer, String, DateTime, Enum as SQLAlchemyEnum
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

# from sqlalchemy.ext.declarative import declarative_base
from passlib.context import CryptContext
from enum import Enum
from pydantic_settings import BaseSettings, SettingsConfigDict
from datetime import datetime
from typing import Optional
import asyncio


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
Base = declarative_base()


class UserRole(Enum):
    ADMIN = "admin"
    USER = "user"
    MODERATOR = "moderator"


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
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
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
        

# --- Schema pre vytvorenie tabuliek v databáze ---
class Settings(BaseSettings):
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_SERVER: str
    MAIL_PORT: int
    MAIL_FROM: str
    MAIL_FROM_NAME: str
    MAIL_STARTTLS: bool = True
    MAIL_SSL_TLS: bool = False
    USE_CREDENTIALS: bool = True
    VALIDATE_CERTS: bool = True
    JWT_ALGORITHM: str
    JWT_SALT: str
    JWT_SECRET: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    SECRET_KEY: str
    DOMAIN: str
    SQLALCHEMY_DATABASE_URL: str
    BASE_URL: str
    
    model_config = SettingsConfigDict(env_file="backend/.env", env_file_encoding="utf-8", extra="ignore")


Config = Settings()

# Vytvorenie asynchrónneho databázového enginu
engine = create_async_engine(Config.SQLALCHEMY_DATABASE_URL, echo=True)

# Vytvorenie asynchrónnych relácií (sessions)
async_session = sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=engine, 
    class_=AsyncSession
)


# --- Funkcia na vygenerovanie tabuliek v databáze ---
async def init_db():
    async with engine.begin() as conn:
        # Vytvorí všetky tabuľky definované v Base
        await conn.run_sync(Base.metadata.create_all)

# Spusti inicializáciu databázy a vytvori tabulky
# asyncio.run(init_db())


# --- Asynchrónna funkcia na získanie databázovej session ---
async def get_db():
    async with async_session() as session:  # Otvorenie session asynchrónne
        try:
            yield session  # Vrátenie session pre použitie
            await session.commit()  # Zatvorenie transakcie
        except Exception:
            await session.rollback()  # Zatvorenie transakcie
            raise
        finally:
            await session.close()  # Asynchrónne zatvorenie session


