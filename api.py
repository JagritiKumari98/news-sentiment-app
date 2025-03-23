from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from utils.text_summarization import summarize_text
from utils.text_to_speech import text_to_speech
from utils.news_scraper import scrape_news  
from utils.sentiment_analysis import analyze_sentiment, comparative_sentiment_analysis  

app = FastAPI()

class TextInput(BaseModel):
    text: str

@app.post("/summarize")
def summarize(input_text: TextInput):
    """
    Fetches news articles, summarizes them, performs sentiment analysis, 
    and provides a comparative sentiment report.
    """
    # Fetch News Articles
    articles = scrape_news(input_text.text)

    if not articles:
        raise HTTPException(status_code=404, detail="No articles found!")

    # Process Each Article
    processed_articles = []
    for article in articles:
        if not article.get("content"):
            continue  # Skip if content is missing

        summary = summarize_text(article["content"])
        sentiment_result = analyze_sentiment(article["content"])

        processed_articles.append({
            "Title": article.get("title", "No Title"),
            "URL": article.get("url", ""),
            "Summary": summary,
            "Sentiment": sentiment_result["sentiment"],
            "Sentiment Score": sentiment_result["score"],
        })

    if not processed_articles:
        raise HTTPException(status_code=404, detail="No valid articles with content found!")

    # Perform Comparative Sentiment Analysis
    sentiment_summary = comparative_sentiment_analysis(processed_articles)

    return {
        "Articles": processed_articles,
        "Comparative Sentiment Analysis": sentiment_summary
    }

@app.post("/text-to-speech")
def tts(input_text: TextInput):
    """
    Converts summarized text to Hindi speech and returns the audio file path.
    """
    if not input_text.text.strip():
        raise HTTPException(status_code=400, detail="Text input is empty!")

    audio_path = text_to_speech(input_text.text)
    
    if not audio_path:
        raise HTTPException(status_code=500, detail="Text-to-Speech conversion failed.")

    return {"audio_path": audio_path}
