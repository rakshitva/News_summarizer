import gradio as gr
from utils import get_ticker, get_news, summarize_text, analyze_sentiment, text_to_speech
import os
import uuid

# Store summarized news for querying
news_database = []

# Function to Fetch News
def gradio_fetch_news(company):
    """Fetch news, summarize, analyze sentiment, and store for querying."""
    
    ticker = get_ticker(company)
    if not ticker:
        return "⚠️ Company not found!"
    
    articles = get_news(company)
    if not articles:
        return "⚠️ No news found!"

    results = []

    for i, article in enumerate(articles):
        summary = summarize_text(article["content"])
        sentiment, sentiment_score = analyze_sentiment(article["content"])
        
        # Generate unique filename for TTS
        unique_id = str(uuid.uuid4())
        audio_file = text_to_speech(summary, filename=f"static/news_{unique_id}.mp3")
        audio_link = f'<a href="file/static/news_{unique_id}.mp3" target="_blank">🎙️ Listen to Hindi Audio Summary</a>'

        # Store in database for querying
        news_database.append({
            "title": article["title"],
            "summary": summary,
            "sentiment": sentiment,
            "sentiment_score": sentiment_score,
            "date": article["date"],
            "audio_file": f"static/news_{unique_id}.mp3"
        })

        title = f"### 📰 {article['title']}"
        summary_text = f"📖 **Summary:**\n{summary}"  
        sentiment_text = f"📊 **Sentiment:** {sentiment} ({sentiment_score:.2f})"

        # Append summary with audio link
        results.append(f"{title}\n\n{summary_text}\n\n{sentiment_text}\n\n{audio_link}\n\n---\n")

    return "\n".join(results)

# Function to Search News
def query_news(keyword, min_sentiment=-1, max_sentiment=1):
    """Search news based on keyword and sentiment score range."""
    filtered_news = [
        article for article in news_database 
        if keyword.lower() in article["summary"].lower() 
        and min_sentiment <= article["sentiment_score"] <= max_sentiment
    ]
    
    if not filtered_news:
        return "❌ No matching news found."
    
    results = []
    for article in filtered_news:
        title = f"### 📰 {article['title']}"
        summary_text = f"📖 **Summary:** {article['summary']}"  
        sentiment_text = f"📊 **Sentiment:** {article['sentiment']} ({article['sentiment_score']:.2f})"
        audio_link = f'<a href="file/{article["audio_file"]}" target="_blank">🎙️ Play Audio</a>'

        results.append(f"{title}\n\n{summary_text}\n\n{sentiment_text}\n\n{audio_link}\n\n---\n")

    return "\n".join(results)

# Gradio Interface
demo = gr.Interface(
    fn=gradio_fetch_news,
    inputs=gr.Textbox(label="Enter Company Name"),
    outputs=gr.Markdown(),
    title="📢 News Summarizer & Sentiment Analyzer"
)

query_interface = gr.Interface(
    fn=query_news,
    inputs=[
        gr.Textbox(label="Enter Keyword"),
        gr.Slider(minimum=-1, maximum=1, step=0.1, label="Min Sentiment Score"),
        gr.Slider(minimum=-1, maximum=1, step=0.1, label="Max Sentiment Score")
    ],
    outputs=gr.Markdown(),
    title="🔍 Query News Stories",
    description="Search for news articles based on keywords and sentiment scores."
)

gr.TabbedInterface([demo, query_interface], ["📢 News Fetcher", "🔍 Query System"]).launch()
