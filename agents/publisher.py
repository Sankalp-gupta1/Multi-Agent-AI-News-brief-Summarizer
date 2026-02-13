import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from dotenv import load_dotenv
from openai import OpenAI
from mcp_servers.media_server import get_image
from mcp_servers.weather_server import get_weather
from mcp_servers.news_server import get_news
from mcp_servers.finance_server import get_finance
from datetime import datetime

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)


def clean_text(text):
    if not text:
        return "No verified data available."
    return " ".join(str(text).split())


def generate_article(topic: str, tone: str = "Analytical", city: str = "Delhi"):

    today = datetime.now().strftime("%A, %B %d, %Y")

    # -------- REGION LOGIC -------- #
    if city.lower() == "india":
        weather_city = "New Delhi"
        finance_market = "india"
        news_query = f"{topic} India stock market"
    else:
        weather_city = city
        finance_market = "global"
        news_query = topic

    # -------- NEWS -------- #
    try:
        news_raw = get_news(news_query)
        news_data = clean_text(news_raw)
    except:
        news_data = "No verified news data available."

    # -------- WEATHER -------- #
    try:
        weather = get_weather(weather_city)
        if isinstance(weather, dict):
            weather_data = f"""
Condition: {weather.get('description', 'N/A')}
Temperature: {weather.get('temperature', 'N/A')}°C
Location: {weather.get('city', weather_city)}
"""
        else:
            weather_data = "Weather data not available."
    except:
        weather_data = "Weather data not available."

    # -------- FINANCE -------- #
    try:
        finance = get_finance(market=finance_market)
        if isinstance(finance, dict) and "error" not in finance:
            finance_data = f"""
Index: {finance.get('index')}
Current Level: {finance.get('price')}
Change: {finance.get('change')}
Status: {finance.get('status')}
"""
        else:
            finance_data = "Financial data not available."
    except:
        finance_data = "Financial data not available."

    # -------- PROMPT -------- #
    prompt = f"""
You are a professional global intelligence analyst.

STRICT RULES:
- Use ONLY verified data provided below.
- Do NOT invent numbers.
- If missing data, clearly state: Information not available.

DATE: {today}
TOPIC: {topic}
REGION: {city}

------------------
NEWS DATA:
{news_data}
------------------

FINANCE DATA:
{finance_data}
------------------

WEATHER DATA:
{weather_data}
------------------

Write a structured intelligence report with sections:

1. Executive Overview
2. Market & Financial Analysis
3. Environmental Context
4. Risk Assessment
5. Strategic Outlook

Tone: {tone}
Professional and analytical.
"""

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You are a strict factual intelligence analyst."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2
        )

        article = response.choices[0].message.content

    except Exception as e:
        return f"AI generation failed: {str(e)}", None

    try:
        image_url = get_image(topic=topic)
    except:
        image_url = None

    return article, image_url


if __name__ == "__main__":
    article, image = generate_article(
        topic="Market crash",
        tone="Formal",
        city="India"
    )

    print("\nARTICLE:\n")
    print(article)
    print("\nIMAGE:\n")
    print(image)



# import sys
# import os
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# from dotenv import load_dotenv
# from openai import OpenAI
# from mcp_servers.media_server import get_image
# from mcp_servers.weather_server import get_weather
# from mcp_servers.news_server import get_news
# from mcp_servers.finance_server import get_finance
# from datetime import datetime

# load_dotenv()

# # ---------------- GROQ CLIENT ---------------- #
# client = OpenAI(
#     api_key=os.getenv("GROQ_API_KEY"),
#     base_url="https://api.groq.com/openai/v1"
# )


# def generate_article(topic: str, tone: str = "Analytical", city: str = "Delhi"):

#     today = datetime.now().strftime("%A, %B %d, %Y")

#     # ---------------- SMART REGION FIX ---------------- #
#     if city.lower() == "india":
#         weather_city = "New Delhi"
#         finance_market = "india"
#     else:
#         weather_city = city
#         finance_market = "global"

#     # ---------------- FETCH NEWS ---------------- #
#     try:
#         news_data = get_news(topic)
#         if not news_data:
#             news_data = "No verified news data available."
#     except Exception:
#         news_data = "No verified news data available."

#     # ---------------- FETCH WEATHER ---------------- #
#     try:
#         weather = get_weather(weather_city)

#         if isinstance(weather, dict):
#             weather_data = f"""
# Condition: {weather.get('description', 'Not available')}
# Temperature: {weather.get('temperature', 'N/A')}°C
# Location: {weather.get('city', weather_city)}
# """
#         else:
#             weather_data = "Weather data not available."

#     except Exception:
#         weather_data = "Weather data not available."

#     # ---------------- FETCH FINANCE ---------------- #
#     try:
#         finance = get_finance(market=finance_market)

#         if isinstance(finance, dict):
#             finance_data = f"""
# Market: {finance.get('index', 'N/A')}
# Current Level: {finance.get('price', 'N/A')}
# Change: {finance.get('change', 'N/A')}
# Status: {finance.get('status', 'N/A')}
# """
#         else:
#             finance_data = "Financial data not available."

#     except Exception:
#         finance_data = "Financial data not available."

#     # ---------------- STRICT INTELLIGENCE PROMPT ---------------- #
#     prompt = f"""
# You are a professional global intelligence analyst.

# STRICT RULES:
# - Use ONLY verified data provided below.
# - Do NOT invent numbers or events.
# - If information missing, clearly state: Information not available.

# DATE: {today}
# TOPIC: {topic}
# REGION: {city}

# -------------------------
# VERIFIED NEWS DATA:
# {news_data}
# -------------------------

# VERIFIED FINANCE DATA:
# {finance_data}
# -------------------------

# VERIFIED WEATHER DATA:
# {weather_data}
# -------------------------

# Write a structured intelligence report with the following sections:

# 1. Executive Overview
# 2. Market & Financial Analysis
# 3. Environmental / Weather Context
# 4. Risk Assessment
# 5. Strategic Outlook

# Tone: {tone}
# Keep it professional and analytical.
# """

#     # ---------------- AI GENERATION ---------------- #
#     try:
#         response = client.chat.completions.create(
#             model="llama-3.1-8b-instant",
#             messages=[
#                 {"role": "system", "content": "You are a strict factual intelligence analyst."},
#                 {"role": "user", "content": prompt}
#             ],
#             temperature=0.2
#         )

#         article = response.choices[0].message.content

#     except Exception as e:
#         return f"AI generation failed: {str(e)}", None

#     # ---------------- IMAGE ---------------- #
#     try:
#         image_url = get_image(topic=topic)
#     except Exception:
#         image_url = None

#     return article, image_url


# # ---------------- TEST ---------------- #
# if __name__ == "__main__":
#     article, image = generate_article(
#         topic="Market crash",
#         tone="Formal",
#         city="India"
#     )

#     print("\nARTICLE:\n")
#     print(article)

#     print("\nIMAGE:\n")
#     print(image)



# import sys
# import os
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# from dotenv import load_dotenv
# from openai import OpenAI
# from mcp_servers.media_server import get_image
# from mcp_servers.weather_server import get_weather
# from mcp_servers.news_server import get_news
# from mcp_servers.finance_server import get_finance
# from datetime import datetime

# load_dotenv()

# # ---------------- GROQ CLIENT ---------------- #
# client = OpenAI(
#     api_key=os.getenv("GROQ_API_KEY"),
#     base_url="https://api.groq.com/openai/v1"
# )


# def generate_article(topic: str, tone: str = "Analytical", city: str = "Delhi"):

#     today = datetime.now().strftime("%A, %B %d, %Y")

#     # ---------------- SAFE DATA FETCH ---------------- #

#     # NEWS
#     try:
#         news_data = get_news(topic)
#         if not news_data:
#             news_data = "No verified news data available."
#     except Exception:
#         news_data = "No verified news data available."

#     # WEATHER
#     try:
#         weather = get_weather(city)

#         if isinstance(weather, dict):
#             weather_info = f"""
# Weather Condition: {weather.get('description', 'Not available')}
# Temperature: {weather.get('temperature', 'N/A')}°C
# Location: {weather.get('city', city)}
# """
#         else:
#             weather_info = "Weather data not available."

#     except Exception:
#         weather_info = "Weather data not available."

#     # FINANCE
#     try:
#         finance_data = get_finance()
#         if not finance_data:
#             finance_data = "Financial data not available."
#     except Exception:
#         finance_data = "Financial data not available."

#     # ---------------- STRICT PROMPT ---------------- #
#     prompt = f"""
# You are a professional factual intelligence editor.

# IMPORTANT RULES:
# - Use ONLY the real data provided below.
# - Do NOT invent names, numbers, or events.
# - If information is missing, say 'Information not available.'

# DATE: {today}

# TOPIC: {topic}

# REAL NEWS DATA:
# {news_data}

# FINANCE DATA:
# {finance_data}

# WEATHER DATA:
# {weather_info}

# Write a structured, professional, concise intelligence brief in a {tone} tone.
# Include clear section headings.
# """

#     # ---------------- AI CALL ---------------- #
#     try:
#         response = client.chat.completions.create(
#             model="llama-3.1-8b-instant",
#             messages=[
#                 {"role": "system", "content": "You are a strict factual intelligence editor."},
#                 {"role": "user", "content": prompt}
#             ],
#             temperature=0.2
#         )

#         article = response.choices[0].message.content

#     except Exception as e:
#         return f"AI generation failed: {str(e)}", None

#     # ---------------- IMAGE ---------------- #
#     try:
#         image_url = get_image(topic=topic)
#     except Exception:
#         image_url = None

#     return article, image_url


# # ---------------- TEST ---------------- #
# if __name__ == "__main__":
#     article, image = generate_article(
#         topic="Delhi Pollution Crisis",
#         tone="Formal",
#         city="Delhi"
#     )

#     print("\nARTICLE:\n")
#     print(article)

#     print("\nIMAGE:\n")
#     print(image)


# import os
# from dotenv import load_dotenv
# from openai import OpenAI
# from mcp_servers.media_server import get_image
# from mcp_servers.weather_server import get_weather
# from datetime import datetime

# load_dotenv()

# # ---------------- GROQ CLIENT ---------------- #
# client = OpenAI(
#     api_key=os.getenv("GROQ_API_KEY"),
#     base_url="https://api.groq.com/openai/v1"
# )

# def generate_article(
#     topic: str,
#     tone: str = "Analytical",
#     city: str = "Delhi"
# ):
#     """
#     Generates a professional newspaper-style article
#     including real weather data.
#     """

#     today = datetime.now().strftime("%A, %B %d, %Y")

#     # ---------------- GET REAL WEATHER ---------------- #
#     weather = get_weather(city)

#     if isinstance(weather, dict):
#         weather_info = f"""
#         Weather Condition: {weather['description']}
#         Temperature: {weather['temperature']}°C
#         Location: {weather['city']}
#         """
#     else:
#         weather_info = weather  # fallback string

#     # ---------------- AI PROMPT ---------------- #
#     prompt = f"""
#     Write a professional newspaper-style news brief strictly focused on:

#     {topic}

#     Date: {today}

#     Include the following verified weather data in the report:
#     {weather_info}

#     Do NOT include unrelated global headlines.
#     Write in a {tone} tone.
#     Keep it structured, journalistic, and concise.
#     """

#     # ---------------- AI CALL ---------------- #
#     response = client.chat.completions.create(
#         model="llama-3.1-8b-instant",
#         messages=[
#             {"role": "system", "content": "You are a professional news editor."},
#             {"role": "user", "content": prompt}
#         ],
#         temperature=0.7
#     )

#     article = response.choices[0].message.content

#     # ---------------- IMAGE ---------------- #
#     image_url = get_image(topic=topic)

#     return article, image_url


# # ---------------- TEST ---------------- #
# if __name__ == "__main__":
#     article, image = generate_article(
#         topic="Delhi Pollution Crisis Intensifies",
#         tone="Formal",
#         city="Delhi"
#     )

#     print("\nARTICLE:\n")
#     print(article)
#     print("\nIMAGE:\n")
#     print(image)


 