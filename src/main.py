"""Main entry point for the trend tracker."""
from datetime import datetime
import pytz

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
    print("📊 Fetching trends from getdaytrends.com...")
    fetch_result = trend_fetcher.fetch_trends()
    trends = fetch_result[0]
    most_tweeted_trends = fetch_result[3] if len(fetch_result) > 3 else None
    longest_trending_trends = fetch_result[4] if len(fetch_result) > 4 else None

    if not trends:
        print("❌ Failed to fetch trends")
        return False

    print(f"✅ Found {len(trends)} trends")
    if most_tweeted_trends:
        print(f"✅ Found {len(most_tweeted_trends)} most tweeted (24h) trends")
    if longest_trending_trends:
        print(f"✅ Found {len(longest_trending_trends)} longest trending trends")

    # Get current timestamp for email in both short and long formats
    paris_tz = pytz.timezone('Europe/Paris')
    now = datetime.now(paris_tz)
    timestamp_str = now.strftime("%I:%M %p")  # Short format for subject
    timestamp_long_str = now.strftime("%A, %B %d, %Y at %I:%M %p")  # Long format for body

    # Store and check trends in Firestore
    trends_collection = db.collection("trend_snapshots")
    trends_doc = trends_collection.document("latest")
    doc = trends_doc.get()
    current_trend_names = [t['name'] for t in trends]
    send_email = True
    if doc.exists and doc.to_dict() is not None:
        prev_trends = doc.to_dict().get("trend_names", [])
        if set(prev_trends) == set(current_trend_names):
            print("⏩ Trends unchanged. Skipping email.")
            send_email = False
    if send_email:
        print("📧 Sending email...")
        success = email_service.send_notification(trends, timestamp_str, most_tweeted_trends, longest_trending_trends, timestamp_long_str)
        if success:
            trends_doc.set({"trend_names": current_trend_names, "timestamp": timestamp_str})
            print("🎉 Trend summary sent successfully!")
            return True
        else:
            print("💥 Failed to send email")
            return False
    return False
