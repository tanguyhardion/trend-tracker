"""HTML generation utilities for trend email notifications."""

import os
from datetime import datetime
from typing import List, Dict, Any
from .config import Config


class HTMLGenerator:
    """Generates HTML content for trend email notifications."""

    def __init__(self):
        self._css_cache = None

    def _load_css(self) -> str:
        """Load CSS content from file with caching."""
        if self._css_cache is None:
            try:
                with open(Config.EMAIL_CSS, "r", encoding="utf-8") as file:
                    self._css_cache = file.read()
            except Exception as e:
                print(f"Error loading CSS file: {e}")
                self._css_cache = ""
        return self._css_cache

    def _create_trend_html(self, trend: Dict[str, Any], index: int) -> str:
        """Create HTML for a single trend."""
        tweet_info = (
            f" <span class='tweet-count'>({trend['tweet_count']})</span>"
            if trend.get("tweet_count")
            else ""
        )

        return f"""
                <div class="trend-item">
                    {index}. <a href='https://x.com/search?q={trend['name']}' target='_blank' class='trend-link'>{trend['name']}</a>{tweet_info}
                </div>"""

    def _create_max_tweets_trend_html(self, trend: Dict[str, Any]) -> str:
        """Create HTML for a single max tweets trend."""
        return f"""
                <div class="max-tweets-item">
                    <a href='https://x.com/search?q={trend['name']}' target='_blank' class='trend-link'>{trend['name']}</a>
                    <span class='tweet-count'>with {trend['tweet_count']}</span>
                </div>"""

    def _create_trends_container(self, trends: List[Dict[str, Any]]) -> str:
        """Create HTML container for all trending topics."""
        trends_html = []
        for i, trend in enumerate(trends, 1):
            trend_html = self._create_trend_html(trend, i)
            trends_html.append(trend_html)

        return f"""
                        <div class="trends-container">
                            <div class="trends-header">
                                <span class="header-text">🔥 All Trending Topics</span>
                                <a href="https://x.com/explore/tabs/trending" target="_blank" class="x-icon-link">𝕏</a>
                            </div>
                            <div class="trends-content">
                                {''.join(trends_html)}
                            </div>
                        </div>"""

    def _create_most_tweeted_container(
        self, most_tweeted_trends: List[Dict[str, Any]]
    ) -> str:
        """Create HTML container for most tweeted (24h) trends."""
        if not most_tweeted_trends:
            return ""

        trends_html = []
        for trend in most_tweeted_trends:
            trend_html = self._create_max_tweets_trend_html(trend)
            trends_html.append(trend_html)

        return f"""
                        <div class="max-tweets-container">
                            <div class="max-tweets-header">📊 Most Tweeted (24h)</div>
                            <div class="max-tweets-content">
                                {''.join(trends_html)}
                            </div>
                        </div>"""

    def _create_longest_trending_container(
        self, longest_trending_trends: List[Dict[str, Any]]
    ) -> str:
        trends_html = []
        for trend in longest_trending_trends:
            trend_html = f"""
                <div class='max-tweets-item'>
                    <a href='https://x.com/search?q={trend['name']}' target='_blank' class='trend-link'>{trend['name']}</a>
                    <span class='tweet-count'>for {trend['time_trending']}</span>
                </div>"""
            trends_html.append(trend_html)
        return f"""
                        <div class="max-tweets-container">
                            <div class="max-tweets-header">⏳ Longest Trending</div>
                            <div class="max-tweets-content">
                                {''.join(trends_html)}
                            </div>
                        </div>"""

    def generate_email_html(
        self,
        trends: List[Dict[str, Any]],
        timestamp: str,
        most_tweeted_trends: List[Dict[str, Any]] = None,
        longest_trending_trends: List[Dict[str, Any]] = None,
    ) -> str:
        css_content = self._load_css()
        trends_container = self._create_trends_container(trends)
        most_tweeted_container = self._create_most_tweeted_container(
            most_tweeted_trends or []
        )
        longest_trending_container = self._create_longest_trending_container(
            longest_trending_trends or []
        )
        return f"""
            <html>
            <head>
                <style>
                    {css_content}
                </style>
            </head>
            <body>
                {trends_container}
                {most_tweeted_container}
                {longest_trending_container}
                <div class="timestamp">
                    <strong>Timestamp:</strong> {timestamp}
                </div>
                <div class="footer">
                    <p><em>This is an automated notification from your trend tracking system.</em></p>
                    <p><small>Click on any trend link to view it on Twitter/X</small></p>
                </div>
            </body>
            </html>
            """
