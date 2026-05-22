from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "NV"
    APP_ENV: str = "development"
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 18000

    OLLAMA_URL: str

    MYSQL_HOST: str
    MYSQL_PORT: int
    MYSQL_USER: str
    MYSQL_PASSWORD: str
    MYSQL_DATABASE: str

    WORKSPACE_ROOT: str = (
        "/home/alex/NV/workspaces/alex"
    )

    class Config:
        env_file = ".env"


settings = Settings()
