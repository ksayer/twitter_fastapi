from pydantic import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "some_project"

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
