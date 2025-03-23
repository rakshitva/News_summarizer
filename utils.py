import os
import requests
import nltk
import yfinance as yf
from bs4 import BeautifulSoup
from nltk.sentiment import SentimentIntensityAnalyzer
from transformers import pipeline
from gtts import gTTS
import torch
from deep_translator import GoogleTranslator  # Use deep_translator instead



# Download NLTK resources
nltk.download("vader_lexicon")

# Load API Keys from environment variables

FINNHUB_API_KEY="cveqnmpr01qjugsebi70cveqnmpr01qjugsebi7g"
NEWS_API_KEY="cefd6269dbc2487092574484e047b2d2"


# Initialize NLP tools
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")
sentiment_analyzer = SentimentIntensityAnalyzer()

def get_ticker(company_name):
    """Fetch stock ticker using Finnhub API or fallback to Yahoo Finance."""
    url = f"https://finnhub.io/api/v1/search?q={company_name}&token={FINNHUB_API_KEY}"
    response = requests.get(url).json()
    
    if "result" in response:
        for stock in response["result"]:
            if stock.get("type") == "Common Stock":
                return stock["symbol"]
    
    # Fallback: Use Yahoo Finance
    try:
        stock = yf.Ticker(company_name)
        return stock.ticker if stock.ticker else None
    except:
        return None

def get_news(company):
    """Fetch latest news articles from NewsAPI."""
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": company,
        "apiKey": NEWS_API_KEY,
        "language": "en",
        "pageSize": 10  # Fetch 10 articles as per requirements
    }
    response = requests.get(url, params=params).json()
    
    if "articles" not in response or not response["articles"]:
        return None
    
    articles = []
    for article in response["articles"]:
        title = article.get("title", "No Title")
        content = article.get("description", "No Content")
        source = article.get("source", {}).get("name", "Unknown")
        url = article.get("url", "")
        date = article.get("publishedAt", "Unknown Date")
        
        articles.append({
            "title": title,
            "content": content,
            "source": source,
            "url": url,
            "date": date
        })
    
    return articles

def summarize_text(text):
    """Summarize long news content using Hugging Face transformers."""
    if not text or len(text.split()) < 50:
        return text or "No summary available."
    summary = summarizer(text, max_length=100, min_length=30, do_sample=False)
    return summary[0]["summary_text"]

def analyze_sentiment(text):
    """Perform sentiment analysis using NLTK."""
    if not text:
        return "Neutral"
    sentiment_score = sentiment_analyzer.polarity_scores(text)
    if sentiment_score["compound"] >= 0.05:
        return "Positive"
    elif sentiment_score["compound"] <= -0.05:
        return "Negative"
    else:
        return "Neutral"

from gtts import gTTS

from gtts import gTTS
from googletrans import Translator  # Import Google Translate API

translator = Translator()  # Initialize the translator
from deep_translator import GoogleTranslator  # Replace googletrans

def text_to_speech(text, filename="static/news_summary.mp3"):
    """Convert summarized text to Hindi speech and save as an MP3 file."""
    if not text:
        return None

    try:
        # Translate English text to Hindi
        translated_text = GoogleTranslator(source="en", target="hi").translate(text)

        # Convert Hindi text to speech
        tts = gTTS(translated_text, lang="hi")
        tts.save(filename)

        return filename  # Return the file path
    except Exception as e:
        print(f"⚠️ Error in TTS: {e}")
        return None


if __name__ == "__main__":
    company = input("Enter company name: ").strip().title()
    
    ticker = get_ticker(company)
    if not ticker:
        print("⚠️ Could not find a ticker for the given company.")
        exit()
    
    print(f"✅ Found Ticker: {ticker}")
    news_articles = get_news(company)
    
    if not news_articles:
        print("⚠️ No news found for the given company.")
        exit()
    
    print("📰 Latest News:")
    for i, article in enumerate(news_articles, 1):
        print(f"\n🔹 Article {i}:")
        print(f"Title: {article['title']}")
        print(f"Source: {article['source']}")
        print(f"URL: {article['url']}")
        print(f"📅 Date: {article['date']}")
        
        summary = summarize_text(article["content"])
        sentiment = analyze_sentiment(article["content"])
        print(f"📝 Summary: {summary}")
        print(f"📊 Sentiment: {sentiment}")
        
        # Generate Hindi TTS
        audio_file = text_to_speech(summary, filename=f"static/news_{i}.mp3")
        print(f"🎙️ Hindi Speech Saved: {audio_file}")
    
    print("\n✅ News processing completed!")
