from dotenv import load_dotenv
import os
import time
import datetime
import webbrowser
import threading
import string
import requests
from flask import Flask, render_template, jsonify
import speech_recognition as sr
import pyttsx3
from google import genai
load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")

app = Flask(__name__, template_folder=TEMPLATE_DIR)
recognizer = sr.Recognizer()

last_bot_response = "I haven't answered any commands yet."

# Initialize Google GenAI Client
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
ai_client = genai.Client(api_key=GEMINI_API_KEY)

def speak(text: str):
    """Text-to-speech feedback using pyttsx3 in a background thread."""
    def _speak_thread():
        try:
            engine = pyttsx3.init()
            engine.say(text)
            engine.runAndWait()
        except Exception as e:
            print(f"[TTS Error] {e}")

    threading.Thread(target=_speak_thread).start()

def get_coordinates(city_name):
    """Get latitude and longitude for a city using Open-Meteo Geocoding API."""
    try:
        url = f"https://geocoding-api.open-meteo.com/v1/search?name={city_name}&count=1&language=en&format=json"
        res = requests.get(url, timeout=5).json()
        if "results" in res and len(res["results"]) > 0:
            location = res["results"][0]
            return location["latitude"], location["longitude"], location["name"], location.get("country", "")
    except Exception:
        pass
    return None, None, None, None

def fetch_weather(user_input=""):
    """Fetches exact live weather using Open-Meteo API."""
    try:
        clean_city = user_input.lower()
        for phrase in ["what is the weather in", "what is the weather for", "weather in", "weather for", "temperature in", "temperature for", "weather", "temperature"]:
            clean_city = clean_city.replace(phrase, "").strip()

        if not clean_city:
            clean_city = "Karachi"

        lat, lon, city_official, country = get_coordinates(clean_city)

        if lat is None:
            return f"Sorry, I couldn't find location coordinates for '{clean_city}'."

        weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
        w_res = requests.get(weather_url, timeout=5).json()
        
        if "current_weather" in w_res:
            temp = w_res["current_weather"]["temperature"]
            wind = w_res["current_weather"]["windspeed"]
            location_label = f"{city_official}, {country}" if country else city_official
            return f"The current temperature in {location_label} is {temp} degrees Celsius with wind speeds of {wind} km per hour."
        else:
            return f"Sorry, could not fetch live weather details for {city_official}."

    except Exception:
        return "I encountered an error retrieving weather data."

def fetch_general_knowledge(user_input: str) -> str:
    """Answers general knowledge queries using the google-genai SDK."""
    clean_query = user_input.strip()

    if not clean_query:
        return "Please ask a question."

    try:
        response = ai_client.models.generate_content(
            model="gemini-3.6-flash",
            contents=f"Answer this user question concisely in 1 to 2 simple sentences for voice output: {clean_query}"
        )
        return response.text.strip()
    except Exception as e:
        print(f"[Gemini Error] {e}")
        return f"QA API Error: {e}"

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/favicon.ico')
def favicon():
    return '', 204

@app.route("/listen", methods=["POST"])
def listen_and_process():
    global last_bot_response
    raw_user_text = ""
    
    with sr.Microphone(device_index=1) as source:
        recognizer.energy_threshold = 200
        recognizer.dynamic_energy_threshold = False
        
        try:
            audio = recognizer.listen(source, timeout=12, phrase_time_limit=8)
            raw_user_text = recognizer.recognize_google(audio).lower()
        except sr.WaitTimeoutError:
            error_msg = "Listening timed out. Please click Speak and try again."
            speak(error_msg)
            return jsonify({"user": "", "bot": error_msg})
        except sr.UnknownValueError:
            error_msg = "I couldn't hear or understand you. Please repeat what you said."
            speak(error_msg)
            return jsonify({"user": "", "bot": error_msg})
        except Exception:
            error_msg = "Microphone error occurred. Please try again."
            speak(error_msg)
            return jsonify({"user": "", "bot": error_msg})

    user_text = raw_user_text.translate(str.maketrans("", "", string.punctuation))
    words = user_text.split()
    bot_response = ""

    # 1. Ignore Assistant Self-Listening
    if "couldnt hear or understand" in user_text or "listening timed out" in user_text:
        return jsonify({"user": "", "bot": "Listening ready..."})

    # 2. Repeat Command
    elif any(phrase in user_text for phrase in ["repeat", "say again", "pardon", "what did you say", "again"]):
        bot_response = f"I said: {last_bot_response}"

    # 3. Precise Greeting Check
    elif "hello" in words or "hi" in words or "hey" in words:
        bot_response = "Hello! How can I assist you today?"

    # 4. Time & Date Commands
    elif "tomorrow" in user_text:
        tomorrow_date = datetime.date.today() + datetime.timedelta(days=1)
        bot_response = f"Tomorrow will be {tomorrow_date.strftime('%A, %B %d, %Y')}."

    elif "yesterday" in user_text:
        yesterday_date = datetime.date.today() - datetime.timedelta(days=1)
        bot_response = f"Yesterday was {yesterday_date.strftime('%A, %B %d, %Y')}."

    elif "time" in user_text:
        bot_response = f"The current time is {time.strftime('%I:%M %p')}."

    elif "date" in user_text or "day" in user_text:
        bot_response = f"Today is {time.strftime('%A, %B %d, %Y')}."

    # 5. Live Weather Command
    elif "weather" in user_text or "temperature" in user_text:
        bot_response = fetch_weather(user_text)

    # 6. Desktop Application Automation
    elif "open notepad" in user_text:
        os.system("start notepad.exe")
        bot_response = "Opening Notepad."

    elif "open calculator" in user_text:
        os.system("calc.exe")
        bot_response = "Opening Calculator."

    elif "open cmd" in user_text or "open command prompt" in user_text:
        os.system("start cmd")
        bot_response = "Opening Command Prompt."

    # 7. Open Web Links & Web Search
    elif "open youtube" in user_text:
        webbrowser.open("https://www.youtube.com")
        bot_response = "Opening YouTube."

    elif "search" in user_text:
        clean_query = user_text.replace("search", "").strip()
        for filler in ["a ", "for ", "about "]:
            if clean_query.startswith(filler):
                clean_query = clean_query[len(filler):].strip()

        if clean_query:
            url = f"https://www.google.com/search?q={clean_query}"
            webbrowser.open(url)
            bot_response = f"Searching Google for {clean_query}."
        else:
            bot_response = "What would you like me to search for?"

    # 8. General Knowledge QA Fallback
    else:
        bot_response = fetch_general_knowledge(raw_user_text)

    if not any(phrase in user_text for phrase in ["repeat", "say again", "pardon", "what did you say", "again"]):
        last_bot_response = bot_response

    speak(bot_response)
    return jsonify({"user": raw_user_text, "bot": bot_response})

def open_browser():
    time.sleep(1.5)
    webbrowser.open("http://127.0.0.1:5000")

if __name__ == "__main__":
    print("[System] Starting Voice Assistant Server...", flush=True)
    threading.Thread(target=open_browser).start()
    app.run(host="127.0.0.1", port=5000, debug=False)