from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    POSTGRES_HOST: str = Field()
    POSTGRES_DB: str = Field()
    POSTGRES_EXTERNAL_PORT: str = Field()
    POSTGRES_USER: str = Field()
    POSTGRES_PASSWORD: str = Field()

    IP_ADDRESS: str = Field()

    WG0_INTERFACE: str = Field(default="wg0")
    WG0_ADDRESS: str = Field()
    WG0_LISTEN_PORT: str = Field()
    WG0_PRE_UP: str = Field()
    WG0_POST_UP: str = Field()
    WG0_PRE_DOWN: str = Field()
    WG0_POST_DOWN: str = Field()

    WG_START_CLIENT_IP: str = Field()
    WG_CLIENT_SUBNET: str = Field()

    model_config = SettingsConfigDict(env_prefix="WG_SERVICE_", env_file=".env")

    def get_postgres_url_migrate(self):
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}/{self.POSTGRES_DB}"

    def get_postgres_url(self):
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}/{self.POSTGRES_DB}"


settings = Settings()  # type: ignore
