import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("NEWS_API_KEY")

def get_news(topic):
    try:
        url = "https://newsapi.org/v2/everything"

        params = {
            "q": topic,
            "language": "en",
            "sortBy": "publishedAt",
            "pageSize": 3,
            "apiKey": API_KEY
        }

        response = requests.get(url, params=params)

        if response.status_code != 200:
            return "News API error."

        data = response.json()

        articles = data.get("articles", [])

        if not articles:
            return "No relevant news found."

        formatted_news = ""

        for article in articles:
            formatted_news += f"""
Title: {article.get('title')}
Source: {article.get('source', {}).get('name')}
Description: {article.get('description')}
---
"""

        return formatted_news

    except Exception as e:
        return f"News API Exception: {str(e)}"





# import requests
# import os
# from dotenv import load_dotenv

# load_dotenv()

# API_KEY = os.getenv("NEWS_API_KEY")

# def get_news():
#     try:
#         url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={API_KEY}"
#         response = requests.get(url)

#         # Agar response empty hai
#         if not response.text:
#             return "No response from News API."

#         data = response.json()

#         # Agar API error return kare
#         if data.get("status") != "ok":
#             return f"News API error: {data}"

#         articles = data.get("articles")

#         # Agar articles list hi nahi mili
#         if not isinstance(articles, list) or len(articles) == 0:
#             return "No news articles available right now."

#         first_article = articles[0]

#         return first_article.get("title", "Headline not found.")

#     except Exception as e:
#         return f"News API Exception: {str(e)}"
