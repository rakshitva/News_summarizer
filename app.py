import gradio as gr
import requests
from utils import get_ticker, get_news, summarize_text, analyze_sentiment, text_to_speech

# Unsplash API Configuration
UNSPLASH_ACCESS_KEY = "ci9X9I5vOQagXtaWLKa8WlFgUtnOZSNJM8MufDtgtQ8"  # Replace with your actual Unsplash API Key

def fetch_company_image(company):
    """Fetch an image related to the company from Unsplash."""
    url = f"https://api.unsplash.com/search/photos?query={company}&client_id={UNSPLASH_ACCESS_KEY}&per_page=1"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        if data["results"]:
            return data["results"][0]["urls"]["regular"]  # Return the first image URL
    return None  # Return None if no image is found

def gradio_fetch_news(company):
    """Fetch news, summarize, analyze sentiment, generate Hindi TTS, and fetch an image."""
    ticker = get_ticker(company)
    if not ticker:
        return "⚠️ Company not found!", None, None

    articles = get_news(company)
    if not articles:
        return "⚠️ No news found!", None, None

    results = []
    audio_files = []
    
    for i, article in enumerate(articles):
        summary = summarize_text(article["content"])
        sentiment = analyze_sentiment(article["content"])
        
        # Generate Hindi audio using text-to-speech
        audio_file_path = text_to_speech(summary)
        
        title = f"### 📰 {article['title']}"
        source = f"📌 **Source:** {article['source']}"
        date = f"📅 **Date:** {article['date']}"
        summary_text = f"📖 **Summary:**\n{summary}"
        sentiment_text = f"📊 **Sentiment:** {sentiment}"
        
        results.append(f"{title}\n\n{source}\n{date}\n\n{summary_text}\n\n{sentiment_text}\n\n---\n")
        audio_files.append(audio_file_path)

    # Fetch company-related image
    company_image_url = fetch_company_image(company)

    return "\n".join(results), audio_files, company_image_url

# Gradio Interface
demo = gr.Interface(
    fn=gradio_fetch_news,
    inputs=gr.Textbox(label="Enter Company Name"),
    outputs=[gr.Markdown(), gr.Audio(), gr.Image()],
    title="📢 News Summarizer & Sentiment Analyzer",
    description="Enter a company name to get summarized news, sentiment analysis, and Hindi text-to-speech output. Relevant company images are also displayed."
)

demo.launch()

