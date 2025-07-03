"""Trend fetching utilities for trend tracker."""

import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pytz
from typing import List, Dict, Any, Tuple, Optional


class TrendFetcher:
    """Fetches trends from trends24.in."""

    def __init__(self):
        self.base_url = "https://getdaytrends.com/united-states/"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

    def _extract_main_trends(self, soup) -> List[Dict[str, Any]]:
        """Extract main trends from the getdaytrends.com page, including 'see more' table and tweet counts."""
        trends = []
        # First table (top trends)
        trend_rows = soup.select(
            "#trends > table.table.table-hover.text-left.clickable.ranking.trends.wider.mb-0 > tbody > tr"
        )
        for row in trend_rows:
            name_link = row.select_one("td.main > a")
            tweet_count_div = row.select_one("td.main > div")
            tweet_count = tweet_count_div.text.strip() if tweet_count_div else ""
            if name_link:
                trend_name = name_link.text.strip()
                trend_url = name_link.get("href", "")
                trends.append({"name": trend_name, "url": trend_url, "tweet_count": tweet_count})
        # Second table (see more trends)
        more_trend_rows = soup.select("#moreTrends > tbody > tr")
        for row in more_trend_rows:
            name_link = row.select_one("td.main > a")
            tweet_count_span = row.select_one("td.main > div > span")
            tweet_count = tweet_count_span.text.strip() if tweet_count_span else ""
            if name_link:
                trend_name = name_link.text.strip()
                trend_url = name_link.get("href", "")
                trends.append({"name": trend_name, "url": trend_url, "tweet_count": tweet_count})
        return trends

    def _extract_most_tweeted_trends(self, soup) -> List[Dict[str, Any]]:
        """Extract most tweeted (24h) trends from the right sidebar table."""
        trends = []
        rows = soup.select(
            "body > main > div > div > div.col-12.col-lg-4.mb-2.mb-sm-4.text-center > section > div > div.inset.mb-3 > table > tbody > tr"
        )
        for row in rows:
            name_link = row.select_one("td.main > a")
            tweet_count_td = row.select_one("td.details.small.text-muted.text-right")
            tweet_count = tweet_count_td.text.strip() if tweet_count_td else ""
            if name_link:
                trend_name = name_link.text.strip()
                trend_url = name_link.get("href", "")
                trends.append({"name": trend_name, "url": trend_url, "tweet_count": tweet_count})
        return trends

    def _extract_longest_trending_trends(self, soup) -> List[Dict[str, Any]]:
        """Extract longest trending trends from the sidebar table."""
        trends = []
        rows = soup.select(
            "body > main > div > div > div.col-12.col-lg-4.mb-2.mb-sm-4.text-center > section > div > div:nth-child(3) > table > tbody > tr"
        )
        for row in rows:
            name_link = row.select_one("td.main > a")
            time_trending_td = row.select_one("td.details.small.text-muted.text-right")
            time_trending = time_trending_td.text.strip() if time_trending_td else ""
            if name_link:
                trend_name = name_link.text.strip()
                trend_url = name_link.get("href", "")
                trends.append({"name": trend_name, "url": trend_url, "time_trending": time_trending})
        return trends

    def fetch_trends(
        self,
    ) -> Tuple[
        Optional[List[Dict[str, Any]]],
        Optional[str],
        Optional[str],
        Optional[List[Dict[str, Any]]],
        Optional[List[Dict[str, Any]]],
    ]:
        """
        Fetch trends from getdaytrends.com.

        Returns:
            Tuple of (trends, timestamp_text, full_timestamp_text, most_tweeted_trends, longest_trending_trends)
        """
        try:
            response = requests.get(self.base_url, headers=self.headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, "html.parser")

            # Extract main trends
            trends = self._extract_main_trends(soup)
            # Extract most tweeted (24h) trends
            most_tweeted_trends = self._extract_most_tweeted_trends(soup)
            # Extract longest trending trends
            longest_trending_trends = self._extract_longest_trending_trends(soup)

            return trends, None, None, most_tweeted_trends, longest_trending_trends
        except requests.RequestException as e:
            print(f"Error fetching trends: {e}")
            return None, None, None, None, None
        except Exception as e:
            print(f"Error parsing trends: {e}")
            return None, None, None, None, None
