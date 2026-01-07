from typing import List, Optional
import requests
from html_to_markdown import convert
from .base import BaseScraper, Article


class AntropicArticle(Article):
    pass

class AnthropicScraper(BaseScraper):
    @property
    def rss_urls(self) -> List[str]:
        return [
            "https://raw.githubusercontent.com/Olshansk/rss-feeds/main/feeds/feed_anthropic_news.xml",
            "https://raw.githubusercontent.com/Olshansk/rss-feeds/main/feeds/feed_anthropic_research.xml",
            "https://raw.githubusercontent.com/Olshansk/rss-feeds/main/feeds/feed_anthropic_engineering.xml",
        ]
    
    def get_articles(self, hours: int =24) -> List[AntropicArticle]:
        return [
            AntropicArticle(**article.model_dump())
            for article in super().get_articles(hours=hours)
        ]

    def url_to_markdown(self, url: str) -> Optional[str]:
        try:
            response = requests.get(
                url, headers={"User-Agent": "Mpzilla/5.0"}, timeout=30
                )
            response.raise_for_status()
            html = response.text
            markdown = convert(html)
            return markdown
        except Exception:
            return None
        

if __name__ == "__main__":
    scraper = AnthropicScraper()
    articles: List[AntropicArticle] = scraper.get_articles(hours=1000)
    markdown: str = scraper.url_to_markdown(articles[0].url)
    print(articles)
