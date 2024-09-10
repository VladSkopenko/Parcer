from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    DB_URL: str

    class Config:
        extra = "ignore"
        env_file = "../.env"
        env_file_encoding = "utf-8"


config = Settings()

