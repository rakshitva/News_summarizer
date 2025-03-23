import gradio as gr
import requests

def fetch_news(company):
    """Fetch news, summaries, sentiment, and Hindi TTS from FastAPI backend."""
    url = f"http://127.0.0.1:8000/get_news?company={company}"
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
            <source src="http://127.0.0.1:8000/play-audio?index={i}" type="audio/mpeg">
            Your browser does not support the audio tag.
        </audio>
        """

        results.append(f"{title}\n\n{source}\n{date}\n\n{summary}\n\n{sentiment}\n\n🎙️ **Hindi Audio:** {audio_player}\n\n---\n")

    return "\n".join(results)

# Gradio UI
demo = gr.Interface(
    fn=fetch_news,
    inputs=gr.Textbox(label="Enter Company Name"),
    outputs=gr.Markdown(),  # Ensure correct formatting
    title="📢 News Summarizer & Sentiment Analyzer",
    description="Enter a company name to get summarized news, sentiment analysis, and Hindi text-to-speech output."
)

demo.launch()