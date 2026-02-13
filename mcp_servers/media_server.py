import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("UNSPLASH_API_KEY")

def get_image(topic="news"):
    try:
        url = "https://api.unsplash.com/photos/random"

        params = {
            "query": topic,
            "orientation": "landscape",
            "client_id": API_KEY
        }

        response = requests.get(url, params=params, timeout=10)

        # If API fails
        if response.status_code != 200:
            return "https://picsum.photos/1600/900"

        data = response.json()

        # If response empty
        if "urls" not in data:
            return "https://picsum.photos/1600/900"

        return data["urls"].get("regular", "https://picsum.photos/1600/900")

    except Exception:
        # Fallback image
        return "https://picsum.photos/1600/900"
