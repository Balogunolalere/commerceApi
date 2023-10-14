# config.py
from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl
import os
from dotenv import load_dotenv

# Load the environment variables from the .env file
load_dotenv()

class Settings(BaseSettings):
    # The app name
    app_name: str = "E-commerce"
    # The admin email
    admin_email: str = "admin@ecommerce.com"
    # The secret key for jwt encoding
    secret_key: str = os.getenv("APP_SECRET_KEY")
    # The algorithm for jwt encoding
    algorithm: str = os.getenv("APP_ALGORITHM")
    # The access token expiration time in minutes
    access_token_expire_minutes: int = os.getenv("APP_ACCESS_TOKEN_EXPIRE_MINUTES")
    # The base URL of the web application
    app_url: AnyHttpUrl = "http://127.0.0.1:8000"
    # email username
    email_username: str = os.getenv("APP_EMAIL_USERNAME")
    # email password
    email_password: str = os.getenv("APP_EMAIL_PASSWORD")
    # email host
    email_host: str = os.getenv("APP_EMAIL_HOST")
    # email port
    email_port: int = os.getenv("APP_EMAIL_PORT")
    # deta app key
    deta_app_key: str = os.getenv("DETA_APP_KEY")

# Create a settings instance
settings = Settings()
