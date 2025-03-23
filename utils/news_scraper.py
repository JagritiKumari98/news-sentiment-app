import requests
import os

def scrape_news(company_name):
    """Fetches latest news articles for a given company using NewsAPI."""
    
    api_key = os.getenv("NEWS_API_KEY")
    if not api_key:
        print("❌ Error: NEWS_API_KEY is missing. Set it before running.")
        return []

    url = f"https://newsapi.org/v2/everything?q={company_name}&apiKey={api_key}&language=en&pageSize=10"

    response = requests.get(url)

    if response.status_code != 200:
        print(f"❌ Error: Failed to fetch news (Status Code: {response.status_code})")
        return []

    news_data = response.json()
    articles = []

    for article in news_data.get("articles", []):
        articles.append({
            "title": article.get("title", "No Title"),
            "url": article.get("url", ""),
            "content": article.get("description", "No content available")  # Use description if content is missing
        })

    return articles

# Test the function
if __name__ == "__main__":
    print(scrape_news("Tesla"))
