from typing import List, Callable, Any
from .config import YOUTUBE_CHANNELS
from .scrapers.youtube import YouTubeScrapper, ChannelVideo
from .scrapers.openai import OpenAIScraper
from .scrapers.anthropic import AnthropicScraper
from .database.repository import Repository

def _save_youtube_videos(
        scraper: YouTubeScrapper, repo: Repository, hours: int
        ) -> List[ChannelVideo]:
    videos = []
    video_dict = []
    for channel_id in YOUTUBE_CHANNELS:
        channel_videos = scraper.get_latest_videos(channel_id=channel_id, hours=hours)
        videos.extend(channel_videos)
        video_dict.extend(
            [
                {
                    "video_id": v.video_id,
                    "title": v.title,
                    "url": v.url,
                    "channel_id": channel_id,
                    "published_at": v.published_at,
                    "description": v.description,
                    "transcript": v.transcript
                }
                for v in channel_videos
            ]
        )
        if video_dict:
            repo.bulk_insert_youtube_videos(video_dict)
    return videos

def _save_rss_artcles(
        scraper, repo: Repository, hours: int, save_func: Callable
        ) -> List[Any]:
    articles = scraper.get_articles(hours=hours)
    if articles:
        articles_dict = [
            {
                "guid": a.guid,
                "title": a.title,
                "url": a.url,
                "published_at": a.published_at,
                "description": a.description,
                "category": a.category
            }
            for a in articles
        ]
        save_func(articles_dict)
    return articles

SCRAPER_REGISTRY = [
    ("youtube", YouTubeScrapper(), _save_youtube_videos),
    (
        "openai", 
        OpenAIScraper(),
        lambda s, r, h: _save_rss_artcles(s, r, h, r.bulk_insert_openai_articles),
    ),
    (
        "anthropic", 
        AnthropicScraper(),
        lambda s, r, h: _save_rss_artcles(s, r, h, r.bulk_insert_anthropic_articles),
    ),
]

def run_scrapers(hours: int = 24) -> dict:
    repo = Repository()
    results = {}

    for name, scraper, save_func in SCRAPER_REGISTRY:
        try:
            items = save_func(scraper, repo, hours)
            results[name] =items
        except Exception as e:
            results[name] = []
            print(f"Error scraping {name}: {e}")

    return results    


if __name__ == "__main__":
    results = run_scrapers(hours=24)
    print(f"YouTube Videos: {len(results['youtube'])}")
    print(f"OpenAI Articles: {len(results['openai'])}")
    print(f"Anthropic Articles: {len(results['anthropic'])}")