import os

from dotenv import load_dotenv

load_dotenv()

class Config:
    # API
    API_BASE_URL = os.getenv("API_BASE_URL")
    APP_TOKEN = os.getenv("APP_TOKEN")

    REQUEST_TIMEOUT = os.getenv(os.getenv("REQUEST_TIMEOUT", 10))