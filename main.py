from app.runner import run_scrapers

def main(hours: int = 24, top_n: int = 10):
    results = run_scrapers(hours=hours)

    print(f"\n=== Scraping Results (last {hours} hours) ===")
    print(f"YuoTube videos: {len(results['youtube'])}")
    print(f"OpenAI articles: {len(results['openai'])}")
    print(f"Anthropic articles: {len(results['anthropic'])}")        

    return results


if __name__ == "__main__":
    import sys 
    hours = int(sys.argv[1]) if len(sys.argv) > 1 else 24
    main(hours=hours)
    
    # hours = 24
    # top_n = 10

    # if len(sys.argv) > 1:
    #     hours = int(sys.argv[1])

    # if len(sys.argv) > 2:
    #     top_n = int(sys.argv[2]) 

    # result = main(hours=hours, top_n=top_n)
    # exit(0 if result["success"] else 1)       