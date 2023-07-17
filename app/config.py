from pydantic import BaseSettings


class Settings(BaseSettings):
    db_hostname: str
    db_port: str
    db_password: str
    db_name: str
    db_username: str
    secret_key: str
    algorithm: str
    access_token_expire_time: int

    # pydantic model class to reference .env file
    class Config:
        env_file = ".env"


settings = Settings()  # type: ignore
