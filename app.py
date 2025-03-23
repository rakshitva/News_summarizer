import gradio as gr
from utils import get_ticker, get_news, summarize_text, analyze_sentiment, text_to_speech
import os

# Gradio Function
def gradio_fetch_news(company):
    """Fetch news, summarize, analyze sentiment, and generate TTS audio."""
    ticker = get_ticker(company)
    if not ticker:
        return "⚠️ Company not found!"
    
    articles = get_news(company)
    if not articles:
        return "⚠️ No news found!"

    results = []
    for i, article in enumerate(articles):
        summary = summarize_text(article["content"])
        sentiment = analyze_sentiment(article["content"])
        audio_file = text_to_speech(summary, filename=f"static/news_{i}.mp3")
        
        title = f"### 📰 {article['title']}"
        source = f"📌 **Source:** {article['source']}"
        date = f"📅 **Date:** {article['date']}"
        summary_text = f"📖 **Summary:**\n{summary}"  
        sentiment_text = f"📊 **Sentiment:** {sentiment}"

        # Audio Player
        audio_player = f"""
        <audio controls style="margin-top:10px;">
            <source src="file/{audio_file}" type="audio/mpeg">
            Your browser does not support the audio tag.
        </audio>
        """

        results.append(f"{title}\n\n{source}\n{date}\n\n{summary_text}\n\n{sentiment_text}\n\n🎙️ **Hindi Audio:** {audio_player}\n\n---\n")

    return "\n".join(results)

# Gradio Interface
demo = gr.Interface(
    fn=gradio_fetch_news,
    inputs=gr.Textbox(label="Enter Company Name"),
    outputs=gr.Markdown(),
    title="📢 News Summarizer & Sentiment Analyzer",
    description="Enter a company name to get summarized news, sentiment analysis, and Hindi text-to-speech output."
)

demo.launch()

