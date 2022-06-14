from pydantic import BaseSettings, EmailStr

class Settings(BaseSettings):
  API_HOST: str = "127.0.0.1"
  API_PORT: int = 8000
  API_V1_URL: str = "/api/v1"
  CORS_ORIGINS: list = [ "http://localhost:8081" ]

  TESTS_USERNAME: EmailStr = "jan@fakelog.cf"
  TESTS_PASSWORD: str = "jan123"
  TESTS_HOST: str = "fakelog.cf"
  TESTS_BACKUP_HOST: str = "fakelog.tk"
  TESTS_SSL: bool = False
  TESTS_INVALID_PASSWORD: str = "marzenna123"
  TESTS_SEMESTER: str = "16"
  TESTS_DEVICE_ID: int = 1234

settings = Settings()