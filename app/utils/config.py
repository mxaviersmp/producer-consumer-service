from pydantic import BaseSettings


class Settings(BaseSettings):
    """Application settings."""

    rabbitmq_default_user: str = 'admin'
    rabbitmq_default_pass: str = 'admin'
    rabbitmq_host: str = 'localhost'
    rabbitmq_connection_attempts: int = 10
    rabbitmq_retry_delay: int = 5
    rabbitmq_queue_name: str = 'default'


SETTINGS = Settings()
