import os
from app.config import Config


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # In-memory SQLite database for testing
    SQLALCHEMY_TRACK_MODIFICATIONS = False
