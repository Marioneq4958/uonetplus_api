from pydantic import BaseSettings, EmailStr
import os
import platform
class fg:
    lightgreen = "\x1B[38;5;46m"
    orange = "\x1B[38;5;208m"
    red = "\x1B[38;5;160m"
    rs = "\033[0m"
class Settings(BaseSettings):
  API_HOST: str = "127.0.0.1"
  API_PORT: int = 8000
  API_DEBUG: bool = False
  API_V1_URL: str = "/api/v1"
  PYTHON_VER = platform.python_version()
  if PYTHON_VER == "3.10.4" or PYTHON_VER == "3.10.5":
    try:
      x = os.environ["W_BACKEND_CORS"]
      print(f'{fg.orange}Wykryto zmienną W_BACKEND_CORS!{fg.rs}')
      CORS_ORIGINS: str = x
    except:
      print(f'{fg.lightgreen}Nie wykryto zmiennej W_BACKEND_CORS. Używanie ustawień domyślnych!{fg.rs}')
      CORS_ORIGINS: list = [ "http://localhost:8080" ]
  else:
    raise Exception(f'{fg.red}Twoja wersja pythona to: {PYTHON_VER} a potrzebna jest 3.10.4 lub wyższa!!!{fg.rs}')
  TESTS_USERNAME: EmailStr = "jan@fakelog.cf"
  TESTS_PASSWORD: str = "jan123"
  TESTS_HOST: str = "fakelog.cf"
  TESTS_BACKUP_HOST: str = "fakelog.tk"
  TESTS_SSL: bool = False
  TESTS_INVALID_PASSWORD: str = "marzenna123"
  TESTS_SEMESTER: str = "16"
  TESTS_DEVICE_ID: int = 1234

settings = Settings()
