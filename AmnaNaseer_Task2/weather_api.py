import requests
import os
from dotenv import load_dotenv

# Load variables from .env into the environment
load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

def get_weather(city):
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"   # gives temp in Celsius
    }
    response = requests.get(BASE_URL, params=params)
    return response.json()

# Temporary test block — only runs when you execute this file directly
if __name__ == "__main__":
    data = get_weather("Karachi")
    print(data)
