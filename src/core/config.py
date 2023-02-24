from pydantic import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "some_project"
    DATABASE_URL: str
    API_PREFIX_V1: str

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
