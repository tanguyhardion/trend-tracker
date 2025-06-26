"""Trend fetching utilities for trend tracker."""

import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pytz
from typing import List, Dict, Any, Tuple, Optional


class TrendFetcher:
    """Fetches trends from trends24.in."""

    def __init__(self):
        self.base_url = "https://trends24.in/united-states/"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

    def _extract_timestamp(self, timeline_container) -> Tuple[str, str]:
        """Extract and format timestamp from the timeline container."""
        title_element = timeline_container.select_one("h3.title")
        timestamp_text = "Unknown time"
        full_timestamp_text = "Unknown time"

        if title_element:
            timestamp_text = title_element.text.strip()
            full_timestamp_text = title_element.text.strip()
            timestamp_data = title_element.get("data-timestamp")

            # Convert timestamp to Paris timezone if available
            if timestamp_data:
                try:
                    timestamp_float = float(str(timestamp_data))
                    utc_time = datetime.fromtimestamp(timestamp_float, tz=pytz.UTC)
                    paris_tz = pytz.timezone("Europe/Paris")
                    paris_time = utc_time.astimezone(paris_tz)
                    timestamp_text = paris_time.strftime("Today at %I:%M %p")
                    full_timestamp_text = paris_time.strftime(
                        "%I:%M %p"
                    )
                except (ValueError, TypeError):
                    pass

        return timestamp_text, full_timestamp_text

    def _extract_main_trends(self, timeline_container) -> List[Dict[str, Any]]:
        """Extract main trends from the timeline container."""
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

                trends.append({
                    "name": trend_name,
                    "url": trend_url,
                    "tweet_count": tweet_count
                })

        return trends

    def _extract_max_tweets_trends(self, soup) -> List[Dict[str, Any]]:
        """Extract trends with maximum tweets from the stats section."""
        max_tweets_trends = []
        stats_section = soup.select_one(
            "body > main > div:nth-child(2) > article > div > section:nth-child(2)"
        )

        if stats_section:
            stat_items = stats_section.select("li.stat-card-item")
            for item in stat_items:
                trend_link = item.select_one("a.trend-link")
                if trend_link:
                    trend_name = trend_link.text.strip()
                    trend_url = trend_link.get("href", "")
                    item_text = item.get_text(strip=True)

                    if "with " in item_text:
                        parts = item_text.split("with ")
                        tweet_count = parts[1].strip() if len(parts) > 1 else ""
                    else:
                        tweet_count = ""

                    max_tweets_trends.append({
                        "name": trend_name,
                        "url": trend_url,
                        "tweet_count": tweet_count,
                    })
        else:
            print("Could not find the max tweets stats section")

        return max_tweets_trends

    def fetch_trends(self) -> Tuple[Optional[List[Dict[str, Any]]], Optional[str], Optional[str], Optional[List[Dict[str, Any]]]]:
        """
        Fetch trends from trends24.in.
        
        Returns:
            Tuple of (trends, timestamp_text, full_timestamp_text, max_tweets_trends)
        """
        try:
            response = requests.get(self.base_url, headers=self.headers)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, "html.parser")

            # Find the timeline container with the trends
            timeline_container = soup.select_one(
                "#timeline-container > div.px-2.scroll-smooth.flex.gap-x-4.w-fit.pt-8 > div:nth-child(1)"
            )

            if not timeline_container:
                print("Could not find the trends container")
                return None, None, None, None

            # Extract timestamp
            timestamp_text, full_timestamp_text = self._extract_timestamp(timeline_container)

            # Extract main trends
            trends = self._extract_main_trends(timeline_container)

            # Extract trends with maximum tweets
            max_tweets_trends = self._extract_max_tweets_trends(soup)

            return trends, timestamp_text, full_timestamp_text, max_tweets_trends

        except requests.RequestException as e:
            print(f"Error fetching trends: {e}")
            return None, None, None, None
        except Exception as e:
            print(f"Error parsing trends: {e}")
            return None, None, None, None
