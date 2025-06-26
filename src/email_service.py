"""Email service for sending trend notifications."""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Dict, Any
from .config import Config
from .html_generator import HTMLGenerator


class EmailService:
    """Handles email notifications for trend alerts."""

    def __init__(self):
        self.html_generator = HTMLGenerator()

    def _validate_email_config(self) -> None:
        """Validate email configuration and raise error if invalid."""
        if not Config.has_email_config():
            missing_vars = Config.get_missing_email_vars()
            msg = (
                "Gmail credentials missing - skipping email notification\n"
                f"Required environment variables: {', '.join(missing_vars)}"
            )
            raise ValueError(msg)

    def _create_email_message(
        self, 
        trends: List[Dict[str, Any]], 
        timestamp: str,
        max_tweets_trends: List[Dict[str, Any]] = None
    ) -> MIMEMultipart:
        """Create the email message with HTML content."""
        message = MIMEMultipart("alternative")
        message["Subject"] = f"US Trends Summary - {timestamp}"
        message["From"] = Config.GMAIL_EMAIL
        message["To"] = Config.RECIPIENT_EMAIL

        # Generate HTML content
        html_body = self.html_generator.generate_email_html(
            trends, timestamp, max_tweets_trends
        )
        html_part = MIMEText(html_body, "html")
        message.attach(html_part)

        return message

    def _send_via_smtp(self, message: MIMEMultipart) -> None:
        """Send email via Gmail SMTP."""
        with smtplib.SMTP(Config.SMTP_SERVER, Config.SMTP_PORT) as server:
            server.starttls()  # Enable encryption
            server.login(Config.GMAIL_EMAIL, Config.GMAIL_APP_PASSWORD)
            server.send_message(message)

    def send_notification(
        self, 
        trends: List[Dict[str, Any]], 
        timestamp: str,
        max_tweets_trends: List[Dict[str, Any]] = None
    ) -> bool:
        """
        Send email notification for detected trends.

        Args:
            trends: List of trend dictionaries
            timestamp: Timestamp string for the email
            max_tweets_trends: List of max tweets trend dictionaries

        Returns:
            bool: True if email was sent successfully, False otherwise
        """
        self._validate_email_config()

        if not trends:
            print("No trends to notify about")
            return False

        try:
            message = self._create_email_message(trends, timestamp, max_tweets_trends)
            self._send_via_smtp(message)
            print(f"✅ Email notification sent to {Config.RECIPIENT_EMAIL}")
            return True

        except Exception as e:
            print(f"❌ Failed to send email: {e}")
            return False
