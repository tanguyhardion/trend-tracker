"""Main entry point for the trend tracker."""

from .trend_fetcher import TrendFetcher
from .email_service import EmailService


def run_trend_tracker():
    """Run the trend tracker application."""
    print("🚀 Starting Trend Tracker...")

    # Initialize services
    trend_fetcher = TrendFetcher()
    email_service = EmailService()

    # Fetch trends
    print("📊 Fetching trends from trends24.in...")
    trends, timestamp, full_timestamp, max_tweets_trends = trend_fetcher.fetch_trends()

    if not trends:
        print("❌ Failed to fetch trends")
        return False

    print(f"✅ Found {len(trends)} trends")
    if max_tweets_trends:
        print(f"✅ Found {len(max_tweets_trends)} trends with maximum tweets")

    # Send email
    print("📧 Sending email...")
    success = email_service.send_notification(trends, full_timestamp, max_tweets_trends)

    if success:
        print("🎉 Trend summary sent successfully!")
        return True
    else:
        print("💥 Failed to send email")
        return False
