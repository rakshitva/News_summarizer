import gradio as gr
import requests
from fastapi import FastAPI
import uvicorn
from threading import Thread
from utils import get_ticker, get_news, summarize_text, analyze_sentiment, text_to_speech
from fastapi.responses import FileResponse
import os

# Create FastAPI App
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

# Start FastAPI in a separate thread
def run_fastapi():
    uvicorn.run(app, host="0.0.0.0", port=7860)

Thread(target=run_fastapi, daemon=True).start()

# Gradio UI
def gradio_fetch_news(company):
    """Fetch news from FastAPI and display in Gradio."""
    url = f"http://127.0.0.1:7860/get_news?company={company}"
    response = requests.get(url)

    if response.status_code != 200:
        return "⚠️ Error fetching news! Please try again."

    data = response.json()
    if "error" in data:
        return data["error"]

    articles = data.get("articles", [])
    if not articles:
        return "⚠️ No articles found!"

    results = []
    for i, article in enumerate(articles):
        title = f"### 📰 {article['title']}"
        source = f"📌 **Source:** {article['source']}"
        date = f"📅 **Date:** {article['publishedAt']}"
        summary = f"📖 **Summary:**\n{article['summary']}"  
        sentiment = f"📊 **Sentiment:** {article['sentiment']}"

        # Embed Audio Player
        audio_player = f"""
        <audio controls style="margin-top:10px;">
            <source src="http://127.0.0.1:7860/play-audio?index={i}" type="audio/mpeg">
            Your browser does not support the audio tag.
        </audio>
        """

        results.append(f"{title}\n\n{source}\n{date}\n\n{summary}\n\n{sentiment}\n\n🎙️ **Hindi Audio:** {audio_player}\n\n---\n")

    return "\n".join(results)

# Launch Gradio
demo = gr.Interface(
    fn=gradio_fetch_news,
    inputs=gr.Textbox(label="Enter Company Name"),
    outputs=gr.Markdown(),
    title="📢 News Summarizer & Sentiment Analyzer",
    description="Enter a company name to get summarized news, sentiment analysis, and Hindi text-to-speech output."
)

demo.launch()
