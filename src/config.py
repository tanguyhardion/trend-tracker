"""Configuration settings for the trend tracker."""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Configuration class for trend tracker settings."""

    # Email settings
    GMAIL_EMAIL = os.getenv("GMAIL_EMAIL")
    GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")
    RECIPIENT_EMAIL = os.getenv("RECIPIENT_EMAIL")
    
    # SMTP settings
    SMTP_SERVER = "smtp.gmail.com"
    SMTP_PORT = 587
    
    # File paths
    BASE_DIR = Path(__file__).parent.parent
    EMAIL_CSS = BASE_DIR / "styles" / "email.css"
    
    @classmethod
    def has_email_config(cls) -> bool:
        """Check if all required email configuration is present."""
        return all([
            cls.GMAIL_EMAIL,
            cls.GMAIL_APP_PASSWORD,
            cls.RECIPIENT_EMAIL
        ])
    
    @classmethod
    def get_missing_email_vars(cls) -> list:
        """Get list of missing email environment variables."""
        missing = []
        if not cls.GMAIL_EMAIL:
            missing.append("GMAIL_EMAIL")
        if not cls.GMAIL_APP_PASSWORD:
            missing.append("GMAIL_APP_PASSWORD")
        if not cls.RECIPIENT_EMAIL:
            missing.append("RECIPIENT_EMAIL")
        return missing
