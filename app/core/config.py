from pydantic import BaseSettings, EmailStr
import os


class fg:
    lightgreen = "\x1B[38;5;46m"
    orange = "\x1B[38;5;208m"
    red = "\x1B[38;5;160m"
    rs = "\033[0m"


class Settings(BaseSettings):
    API_HOST: str = "127.0.0.1"
    API_PORT: int = 8000
    API_V1_URL: str = "/api/v1"
    try:
        x = os.environ["W_BACKEND_CORS"]
        print(f'{fg.orange}Checked variable W_BACKEND_CORS!{fg.rs}')
        CORS_ORIGINS: str = x
    except:
        print(f'{fg.lightgreen}Not checked variable W_BACKEND_CORS. Use default settings!{fg.rs}')
        CORS_ORIGINS: list = ["http://localhost:8080"]
    TESTS_USERNAME: EmailStr = "jan@fakelog.cf"
    TESTS_PASSWORD: str = "jan123"
    TESTS_HOST: str = "fakelog.gq"
    TESTS_BACKUP_HOST: str = "fakelog.tk"
    TESTS_SSL: bool = True
    TESTS_INVALID_PASSWORD: str = "marzenna123"
    TESTS_SEMESTER: str = "16"
    TESTS_DEVICE_ID: int = 1234

settings = Settings()
