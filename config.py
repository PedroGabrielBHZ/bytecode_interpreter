import os


class Config:
    """Base configuration."""

    SECRET_KEY = os.environ.get("SECRET_KEY") or "dev-secret-key-change-in-production"
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size


class DevelopmentConfig(Config):
    """Development configuration."""

    DEBUG = True
    ENV = "development"


class ProductionConfig(Config):
    """Production configuration."""

    DEBUG = False
    ENV = "production"
    SECRET_KEY = os.environ.get("SECRET_KEY")


class TestingConfig(Config):
    """Testing configuration."""

    TESTING = True
    DEBUG = True


config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
    "default": DevelopmentConfig,
}
