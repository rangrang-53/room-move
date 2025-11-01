from pydantic_settings import BaseSettings
from typing import List
import os
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    """애플리케이션 설정"""

    # Application
    APP_NAME: str = "RoomMove"
    APP_VERSION: str = "1.0"
    DEBUG: bool = True

    # Database
    DATABASE_URL: str = "sqlite:///./data/database.db"

    # API Keys
    GEMINI_API_KEY: str = ""
    NAVER_CLIENT_ID: str = ""
    NAVER_CLIENT_SECRET: str = ""
    EXA_API_KEY: str = ""

    # LangSmith
    LANGSMITH_API_KEY: str = ""
    LANGSMITH_PROJECT: str = "roommove"

    # Session
    SECRET_KEY: str = "change-this-in-production"

    # CORS - 문자열로 받아서 나중에 파싱
    ALLOWED_ORIGINS: str = "http://localhost:8501,http://127.0.0.1:8501"

    class Config:
        case_sensitive = True
        env_file = ".env"


# Settings 인스턴스 생성
_settings = Settings()

# ALLOWED_ORIGINS를 리스트로 변환
class AppSettings:
    def __init__(self, settings: Settings):
        self.APP_NAME = settings.APP_NAME
        self.APP_VERSION = settings.APP_VERSION
        self.DEBUG = settings.DEBUG
        self.DATABASE_URL = settings.DATABASE_URL
        self.GEMINI_API_KEY = settings.GEMINI_API_KEY
        self.NAVER_CLIENT_ID = settings.NAVER_CLIENT_ID
        self.NAVER_CLIENT_SECRET = settings.NAVER_CLIENT_SECRET
        self.EXA_API_KEY = settings.EXA_API_KEY
        self.LANGSMITH_API_KEY = settings.LANGSMITH_API_KEY
        self.LANGSMITH_PROJECT = settings.LANGSMITH_PROJECT
        self.SECRET_KEY = settings.SECRET_KEY
        self.ALLOWED_ORIGINS = [origin.strip() for origin in settings.ALLOWED_ORIGINS.split(",")]


settings = AppSettings(_settings)
