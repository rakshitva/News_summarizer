
# News Summarizer & Sentiment Analyzer

## Overview
This project is designed to fetch and analyze the latest news related to a given company. By providing a company name, the system retrieves relevant news articles, summarizes key information, performs sentiment analysis, and generates an audio summary in Hindi. The goal is to make financial and business news more accessible and easily digestible.

## Features
1. **Retrieves relevant news articles** based on the company name.
2. **Summarizes key points** to provide a concise overview.
3. **Performs sentiment analysis** to classify news as Positive, Negative, or Neutral.
4. **Generates a Hindi audio summary** using text-to-speech (TTS) technology.
5. **User-friendly interface** for seamless interaction.

---

## Implementation Details

### 1. Extracting Company Name & Finding Stock Ticker
- The system processes the input using text tokenization to extract relevant keywords.
- It then utilizes the `yfinance` library to retrieve the stock ticker symbol associated with the company.
- If a valid stock ticker is not found, an appropriate error message is displayed to inform the user.

### 2. Fetching the Latest News
- The application integrates with a news API to fetch recent articles based on the company name.
- Extracted information includes:
  - **Title** of the article, ensuring clarity and relevance.
  - **Publication date** to provide a timeline of events.
  - **Source** to validate credibility and authenticity.
  - **Full article content** to enable detailed analysis.
- If no news articles are available, a notification informs the user accordingly, preventing confusion.

### 3. Summarizing the News
- The summarization process leverages the Hugging Face Transformers library (`transformers`).
- Pre-trained models such as `BART` or `T5` are used to generate concise summaries by extracting key insights.
- The system ensures that only the most relevant information is retained while eliminating redundant details, making the summary easy to understand.

### 4. Sentiment Analysis
- Sentiment analysis is conducted using Natural Language Processing (NLP) with the `nltk` library.
- The news sentiment is classified into three categories:
  - **Positive News** – Indicates favorable developments for the company, potentially boosting investor confidence.
  - **Negative News** – Highlights challenges or risks that may impact business performance or reputation.
  - **Neutral News** – Provides factual updates that do not significantly affect business outlook.
- This categorization allows users to quickly gauge the impact of the news.

### 5. Converting Summary to Audio
- The summarized text is converted into speech using Google Text-to-Speech (`gTTS`).
- The output is in Hindi, catering to users who prefer listening over reading, enhancing accessibility.
- The audio file is generated in MP3 format and can be played directly within the application, offering an alternative way to consume information.

### 6. User Interface
- A web-based interface is developed using `Gradio`, making it easy for users to interact with the system.
- Users can enter a company name and receive structured output that includes:
  - A summarized version of the latest news, eliminating the need to read lengthy articles.
  - Sentiment classification, allowing users to gauge the overall tone of the news.
  - An option to play the Hindi audio summary for those who prefer an auditory experience.
- The application is designed to be intuitive, requiring minimal user effort while delivering maximum value.

---

## Technologies Used
- **`yfinance`** – Fetches stock ticker symbols to enhance accuracy.
- **News API** – Retrieves recent articles to provide up-to-date insights.
- **`transformers`** – Utilizes deep learning models for advanced text summarization.
- **`nltk`** – Performs sentiment analysis to categorize news effectively.
- **`gTTS`** – Converts summarized text into Hindi speech, making content accessible.
- **`gradio`** – Provides a web-based interface for seamless user interaction.

This project is designed to streamline access to business news insights, providing users with clear, summarized, and sentiment-analyzed updates in a simple and effective manner.

