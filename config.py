import os
from dotenv import load_dotenv

# Load environment variables from .env file if available
load_dotenv()

class Config:
    """Base configuration class."""
    SECRET_KEY = os.getenv('SECRET_KEY', 'default-dev-secret-key-change-me')
    MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/student_career_db')
    DB_NAME = os.getenv('DB_NAME', 'student_career_db')
    DEBUG = False
    TESTING = False

class DevelopmentConfig(Config):
    """Development environment configuration."""
    DEBUG = True

class TestingConfig(Config):
    """Testing environment configuration."""
    TESTING = True
    MONGODB_URI = 'mongodb://localhost:27017/student_career_test_db'
    DB_NAME = 'student_career_test_db'

class ProductionConfig(Config):
    """Production environment configuration."""
    DEBUG = False

config_by_name = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
