import os

TOP_DIR = os.path.dirname(os.path.abspath(__file__))

class Config:
    """Base configuration."""
    filename_maxit_version = "maxit-latest-version.txt"
    filepath_maxit_version = os.path.join(TOP_DIR, filename_maxit_version)
    if os.path.isfile(filepath_maxit_version):
        with open(filepath_maxit_version) as file:
            MAXIT_VERSION = file.readline().strip()
    else:
        MAXIT_VERSION = "11.300"

class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False

class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True

class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
