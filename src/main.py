"""Main entry point for the trend tracker."""

from .trend_fetcher import TrendFetcher
from .email_service import EmailService
from .firebase_service import init_firebase


def run_trend_tracker():
    """Run the trend tracker application."""
    print("🚀 Starting Trend Tracker...")

    # Initialize services
    trend_fetcher = TrendFetcher()
    email_service = EmailService()
    db = init_firebase()

    # Fetch trends
    print("📊 Fetching trends from trends24.in...")
    trends, timestamp, full_timestamp, max_tweets_trends = trend_fetcher.fetch_trends()

    if not trends:
        print("❌ Failed to fetch trends")
        return False

    print(f"✅ Found {len(trends)} trends")
    if max_tweets_trends:
        print(f"✅ Found {len(max_tweets_trends)} trends with maximum tweets")

    # Check Firestore for sent timestamp
    sent_ref = db.collection("sent_trend_emails").document(str(full_timestamp))
    sent_doc = sent_ref.get()
    if sent_doc.exists:
        print(f"⏩ Email for timestamp {full_timestamp} already sent. Skipping.")
        return False

    # Send email
    print("📧 Sending email...")
    success = email_service.send_notification(trends, full_timestamp, max_tweets_trends)

    if success:
        sent_ref.set({"timestamp": full_timestamp})
        print("🎉 Trend summary sent successfully!")
        return True
    else:
        print("💥 Failed to send email")
        return False
