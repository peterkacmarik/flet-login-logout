#  # Načítanie konfiguračných údajov pomocou pydantic Settings
 
# from pydantic_settings import BaseSettings, SettingsConfigDict


# class Settings(BaseSettings):
#     API_BASE_URL: str = "http://127.0.0.1:8000/api/v1/auth"
#     AUTH_ENDPOINTS: dict = {
#         "login": API_BASE_URL + "/login",
#         "register": API_BASE_URL + "/register",
#         "protected": API_BASE_URL + "/protected",
#         "logout": API_BASE_URL + "/logout",
#         "verify_token": API_BASE_URL + "/verify-token"
#     }
    
#     model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

        
# frontend_settings = Settings()
# # print(Settings().model_dump())
