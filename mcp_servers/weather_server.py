import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("WEATHER_API_KEY")

def get_weather(city="Delhi"):
    try:
        url = "https://api.openweathermap.org/data/2.5/weather"

        params = {
            "q": city,
            "appid": API_KEY,
            "units": "metric"
        }

        response = requests.get(url, params=params, timeout=10)

        if response.status_code != 200:
            return f"Weather data unavailable for {city}"

        data = response.json()

        temp = data.get("main", {}).get("temp", "N/A")
        description = data.get("weather", [{}])[0].get("description", "No data")

        return {
            "city": city,
            "temperature": temp,
            "description": description
        }

    except Exception:
        return f"Weather service error for {city}"


# import requests
# import os
# from dotenv import load_dotenv

# load_dotenv()

# API_KEY = os.getenv("WEATHER_API_KEY")

# def get_weather():
#     url = f"https://api.openweathermap.org/data/2.5/weather?q=Delhi&appid={API_KEY}&units=metric"
#     response = requests.get(url).json()

#     temp = response["main"]["temp"]
#     description = response["weather"][0]["description"]

#     return f"{description}, {temp}°C in Delhi"
 