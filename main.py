#!/usr/bin/env python3
"""
Trend Tracker - Fetches trends from trends24.in and sends email summary
"""

import os
import smtplib
import requests
from bs4 import BeautifulSoup
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import time
import pytz


def fetch_trends():
    """Fetch trends from trends24.in"""
    url = "https://trends24.in/united-states/"

    try:
        # Add headers to mimic a real browser
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

        response = requests.get(url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, "html.parser")

        # Find the timeline container with the trends
        timeline_container = soup.select_one(
            "#timeline-container > div.px-2.scroll-smooth.flex.gap-x-4.w-fit.pt-8 > div:nth-child(1)"
        )

        if not timeline_container:
            print("Could not find the trends container")
            return None, None, None

        # Extract timestamp
        title_element = timeline_container.select_one("h3.title")
        timestamp_text = "Unknown time"
        full_timestamp_text = "Unknown time"
        timestamp_data = None

        if title_element:
            timestamp_text = title_element.text.strip()
            full_timestamp_text = title_element.text.strip()
            timestamp_data = title_element.get("data-timestamp")

            # Convert timestamp to Paris timezone if available
            if timestamp_data:
                try:
                    # Convert Unix timestamp to datetime in Paris timezone
                    timestamp_float = float(str(timestamp_data))
                    utc_time = datetime.fromtimestamp(timestamp_float, tz=pytz.UTC)
                    paris_tz = pytz.timezone('Europe/Paris')
                    paris_time = utc_time.astimezone(paris_tz)
                    timestamp_text = paris_time.strftime("Today at %I:%M %p")  # For subject
                    full_timestamp_text = paris_time.strftime("%A, %B %d, %Y at %I:%M %p (Paris Time)")  # For email body
                except (ValueError, TypeError):
                    # Keep original text if conversion fails
                    pass

        # Extract trends
        trends = []
        trend_items = timeline_container.select("li")

        for item in trend_items:
            trend_link = item.select_one("a.trend-link")
            tweet_count_span = item.select_one("span.tweet-count")

            if trend_link:
                trend_name = trend_link.text.strip()
                trend_url = trend_link.get("href", "")

                # Get tweet count
                tweet_count = ""
                if tweet_count_span:
                    count_data = tweet_count_span.get("data-count", "")
                    if count_data:
                        tweet_count = tweet_count_span.text.strip()

                trends.append(
                    {"name": trend_name, "url": trend_url, "tweet_count": tweet_count}
                )

        return trends, timestamp_text, full_timestamp_text

    except requests.RequestException as e:
        print(f"Error fetching trends: {e}")
        return None, None, None
    except Exception as e:
        print(f"Error parsing trends: {e}")
        return None, None, None


def format_email_content(trends, timestamp):
    """Format trends data into email content"""
    if not trends:
        return "No trends data available.", "No trends data available."

    html_content = f"""
    <html>
    <head>
        <style>
            body {{
                font-family: Arial, sans-serif;
                line-height: 1.6;
                color: #333;
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
            }}
            h2 {{
                color: #2c3e50;
                border-bottom: 3px solid #3498db;
                padding-bottom: 10px;
            }}
            h3 {{
                color: #495057;
                font-size: 18px;
                margin-top: 30px;
                margin-bottom: 15px;
                font-weight: bold;
            }}
            .main-trends-list {{
                background-color: #f8f9fa;
                border: 1px solid #dee2e6;
                border-radius: 8px;
                padding: 20px;
                margin: 20px 0;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                list-style: decimal;
                padding-left: 40px;
            }}
            .main-trends-list li {{
                margin-bottom: 8px;
                line-height: 1.4;
            }}
            .stat-card {{
                background-color: #f8f9fa;
                border: 1px solid #dee2e6;
                border-radius: 8px;
                padding: 20px;
                margin: 20px 0;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }}
            .stat-card-title {{
                color: #495057;
                font-size: 18px;
                margin-bottom: 15px;
                font-weight: bold;
            }}
            .stat-card-list {{
                list-style: decimal;
                padding-left: 20px;
            }}
            .stat-card-item {{
                margin-bottom: 8px;
                line-height: 1.4;
            }}
            .trend-link {{
                color: #007bff;
                text-decoration: none;
                font-weight: bold;
            }}
            .trend-link:hover {{
                text-decoration: underline;
            }}
            a {{
                color: #007bff;
                text-decoration: none;
            }}
            a:hover {{
                text-decoration: underline;
            }}
        </style>
    </head>
    <body>
        <h2>🔥 Current US Trends Summary</h2>
        
        <h3>All Trending Topics</h3>
        <ol class="main-trends-list">
    """

    text_content = f"🔥 Current US Trends Summary\n\n"
    text_content += "All Trending Topics\n"

    # Show all trends instead of just 20
    for i, trend in enumerate(trends, 1):
        tweet_info = f" ({trend['tweet_count']} tweets)" if trend["tweet_count"] else ""

        html_content += f"""
            <li>
                <strong><a href="{trend['url']}">{trend['name']}</a></strong>
                {tweet_info}
            </li>
        """

        text_content += f"{i}. {trend['name']}{tweet_info}\n"

    html_content += f"""
        </ol>
        
        <h3>Trends with Maximum Tweets</h3>
        <section class="stat-card">
            <ol class="stat-card-list" aria-labelledby="max-tweets-stats">
    """
    
    # Get top trends with highest tweet counts for the new section
    trends_with_counts = [trend for trend in trends if trend.get('tweet_count')]
    # Sort by tweet count (extract numeric value from strings like "7.9M tweet")
    def extract_tweet_number(tweet_count_str):
        try:
            # Remove "tweet" or "tweets" and extract number
            count_str = tweet_count_str.replace(' tweet', '').replace(' tweets', '').strip()
            if 'M' in count_str:
                return float(count_str.replace('M', '')) * 1000000
            elif 'K' in count_str:
                return float(count_str.replace('K', '')) * 1000
            else:
                return float(count_str)
        except:
            return 0
    
    trends_with_counts.sort(key=lambda x: extract_tweet_number(x.get('tweet_count', '0')), reverse=True)
    
    # Show top 5 trends with maximum tweets
    for trend in trends_with_counts[:5]:
        html_content += f"""
                <li class="stat-card-item">
                    <a href="{trend['url']}" class="trend-link">{trend['name']}</a>
                    with {trend['tweet_count']}
                </li>
        """
    
    html_content += f"""
            </ol>
        </section>
        
        <p><strong>Timestamp:</strong> {timestamp}</p>
        
        <hr style="border: none; border-top: 3px solid #333; margin: 20px 0;">
        <p><em>Generated by Trend Tracker</em></p>
    </body>
    </html>
    """

    return html_content, text_content


def send_email(html_content, text_content, timestamp):
    """Send email with trends summary"""

    # Get environment variables
    gmail_email = os.getenv("GMAIL_EMAIL")
    gmail_password = os.getenv("GMAIL_APP_PASSWORD")
    recipient = os.getenv("RECIPIENT_EMAIL")

    if not all([gmail_email, gmail_password, recipient]):
        print("Error: Missing required environment variables:")
        print("- GMAIL_EMAIL", gmail_email)
        print("- GMAIL_APP_PASSWORD", gmail_password)
        print("- RECIPIENT_EMAIL", recipient)
        return False

    try:
        # Create message with timestamp in subject
        msg = MIMEMultipart("alternative")
        msg["Subject"] = f"US Trends Summary - {timestamp}"
        msg["From"] = gmail_email
        msg["To"] = recipient

        # Create text and HTML parts
        text_part = MIMEText(text_content, "plain")
        html_part = MIMEText(html_content, "html")

        msg.attach(text_part)
        msg.attach(html_part)

        # Send email
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(gmail_email, gmail_password)
            server.send_message(msg)

        print(f"✅ Email sent successfully to {recipient}")
        return True

    except Exception as e:
        print(f"❌ Error sending email: {e}")
        return False


def main():
    """Main function"""
    print("🚀 Starting Trend Tracker...")

    # Fetch trends
    print("📊 Fetching trends from trends24.in...")
    trends, timestamp, full_timestamp = fetch_trends()

    if not trends:
        print("❌ Failed to fetch trends")
        return

    print(f"✅ Found {len(trends)} trends")

    # Format email content
    print("📝 Formatting email content...")
    html_content, text_content = format_email_content(trends, full_timestamp)

    # Send email
    print("📧 Sending email...")
    success = send_email(html_content, text_content, timestamp)

    if success:
        print("🎉 Trend summary sent successfully!")
    else:
        print("💥 Failed to send email")


if __name__ == "__main__":
    main()
