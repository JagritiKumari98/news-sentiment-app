from textblob import TextBlob
import json

def analyze_sentiment(text):
    """
    Analyzes the sentiment of the given text using TextBlob.
    Returns 'Positive', 'Negative', or 'Neutral' based on polarity score.
    """
    if not text or text.strip() == "":
        return {"sentiment": "Neutral", "score": 0}  # Handle empty text safely

    blob = TextBlob(text)
    polarity = blob.sentiment.polarity  # Polarity score (-1 to 1)

    if polarity > 0:
        sentiment = "Positive"
    elif polarity < 0:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"

    return {"sentiment": sentiment, "score": round(polarity, 3)}  # Rounding for readability

def comparative_sentiment_analysis(articles):
    """
    Performs comparative sentiment analysis across multiple news articles.
    Returns sentiment distribution and key topic comparisons.
    """
    sentiment_counts = {"Positive": 0, "Negative": 0, "Neutral": 0}
    sentiment_scores = []

    for article in articles:
        if "Summary" not in article or not article["Summary"].strip():
            article["Sentiment"] = "Neutral"
            article["Sentiment Score"] = 0
            continue  # Skip articles without summaries

        sentiment_result = analyze_sentiment(article["Summary"])
        article["Sentiment"] = sentiment_result["sentiment"]
        article["Sentiment Score"] = sentiment_result["score"]
        
        sentiment_counts[sentiment_result["sentiment"]] += 1
        sentiment_scores.append(sentiment_result["score"])

    # Calculate sentiment distribution
    total_articles = max(len(articles), 1)  # Avoid division by zero
    sentiment_distribution = {
        "Positive": sentiment_counts["Positive"],
        "Negative": sentiment_counts["Negative"],
        "Neutral": sentiment_counts["Neutral"],
    }

    # Generate comparison insights
    coverage_differences = []
    if total_articles >= 2:
        for i in range(total_articles - 1):
            coverage_differences.append({
                "Comparison": f"Article {i+1} vs Article {i+2}",
                "Impact": f"Article {i+1} has sentiment {articles[i]['Sentiment']} while Article {i+2} has sentiment {articles[i+1]['Sentiment']}."
            })

    return {
        "Sentiment Distribution": sentiment_distribution,
        "Coverage Differences": coverage_differences
    }

# Example Test
if __name__ == "__main__":
    test_articles = [
        {"Summary": "Tesla's stock is booming, and sales have skyrocketed."},
        {"Summary": "Tesla faces a lawsuit over faulty self-driving software."},
        {"Summary": "Tesla announces a new battery innovation that might change the EV market."},
        {"Summary": ""},  # Empty summary test
        {}  # Missing summary test
    ]
    result = comparative_sentiment_analysis(test_articles)
    print(json.dumps(result, indent=2))
