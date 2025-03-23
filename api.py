from fastapi import FastAPI
from fastapi.responses import FileResponse
import requests
from utils import get_ticker, get_news, summarize_text, analyze_sentiment, text_to_speech
import os

app = FastAPI()

@app.get("/get_news")
def fetch_news(company: str):
    """Fetch news articles, summarize, analyze sentiment, and generate TTS audio."""
    ticker = get_ticker(company)
    if not ticker:
        return {"error": "Company not found"}
    
    articles = get_news(company)
    if not articles:
        return {"error": "No news found"}
    
    processed_articles = []
    for i, article in enumerate(articles):
        summary = summarize_text(article["content"])
        sentiment = analyze_sentiment(article["content"])
        audio_file = text_to_speech(summary, filename=f"static/news_{i}.mp3")
        
        processed_articles.append({
            "title": article["title"],
            "source": article["source"],
            "publishedAt": article["date"],
            "summary": summary,
            "sentiment": sentiment,
            "audio_file": audio_file
        })
    
    return {"company": company, "articles": processed_articles}

@app.get("/play-audio")
def play_audio(index: int):
    """Serve generated audio file."""
    filename = f"static/news_{index}.mp3"
    if os.path.exists(filename):
        return FileResponse(filename, media_type="audio/mpeg")
    return {"error": "Audio file not found"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
