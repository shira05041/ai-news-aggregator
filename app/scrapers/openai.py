from typing import List
from .base import BaseScraper, Article

class OpenAIArticle(Article):
    pass

class OpenAIScraper(BaseScraper):
    @property
    def rss_urls(sef) -> List[str]:
        return ["https://openai.com/news/rss.xml"]
    
    def get_articles(self, hours: int = 24) -> List[OpenAIArticle]:
        return [
            OpenAIArticle(**article.model_dump())
            for article in super().get_articles(hours=hours)
        ]  

if __name__ == "__main__":
    scraper = OpenAIScraper()
    articles: List[OpenAIArticle] = scraper.get_articles(hours=50)     