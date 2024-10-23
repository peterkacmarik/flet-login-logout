#  # Načítanie konfiguračných údajov pomocou pydantic Settings
 
# from pydantic_settings import BaseSettings, SettingsConfigDict


# class Settings(BaseSettings):
#     MAIL_USERNAME: str
#     MAIL_PASSWORD: str
#     MAIL_SERVER: str
#     MAIL_PORT: int
#     MAIL_FROM: str
#     MAIL_FROM_NAME: str
#     MAIL_STARTTLS: bool = True
#     MAIL_SSL_TLS: bool = False
#     USE_CREDENTIALS: bool = True
#     VALIDATE_CERTS: bool = True
#     JWT_ALGORITHM: str
#     JWT_SALT: str
#     JWT_SECRET: str
#     ACCESS_TOKEN_EXPIRE_MINUTES: int
#     SECRET_KEY: str
#     DOMAIN: str
#     SQLALCHEMY_DATABASE_URL: str
#     BASE_URL: str
    
#     model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

        
# Config = Settings()
# # print(Settings().model_dump())