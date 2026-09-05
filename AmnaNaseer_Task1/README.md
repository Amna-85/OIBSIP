### Python Voice Assistant (Flask + Gemini)

A browser-based voice assistant built with Python and Flask. It listens to spoken commands through your microphone, transcribes them to text, matches them against a set of built-in commands, and falls back to Google's Gemini API for open-ended general knowledge questions — replying both on-screen and out loud via text-to-speech.

### Features

**Voice input capture** — records and transcribes speech via the microphone using Google's Speech Recognition API
**Spoken responses**— replies are read aloud using `pyttsx3` text-to-speech, run on a background thread so the app doesn't freeze while speaking
**Greetings** — responds to "hello", "hi", "hey"
**Time & date** — tells the current time, today's date, tomorrow's date, and yesterday's date
**Live weather**— fetches real-time temperature and wind speed for any city using the Open-Meteo API (geocodes the city name to coordinates first, no API key required)
**Web search & YouTube** — opens a Google search directly in your browser based on what you say
**General knowledge Q&A** — any question that doesn't match a built-in command is sent to Google's Gemini API for a natural-language answer
**"Repeat that" command** — repeats the assistant's last response on request
**Simple web interface**— served via Flask, opens automatically in your browser on startup

### Technologies Used

**Python:**Core language 
**Flask:**Web server and browser-based UI 
**Speech_Recognition:**Captures microphone audio and converts it to text (via Google's Web Speech API) 
**pyttsx3:**Converts text responses to spoken audio
**Google Gemini API:**(`google-genai`)-Answers general knowledge questions outside the built-in command set 
**Open-Meteo API:**Free, no-key-required live weather and city geocoding 
**python-dotenv:**Loads API keys from a local `.env` file instead of hardcoding them 
**requests:**Makes HTTP calls to the weather and geocoding APIs 
**threading:**Runs text-to-speech and browser-launch in the background without blocking the app 

 ### Project Structure

```
project-folder/
├── app.py              # main Flask app and voice assistant logic
├── templates/
│   └── index.html      # front-end page served to the browser
├── .env                # your API key (not committed to git)
├── .gitignore           # excludes .env from version control
└── README.md
```

### Setup

### 1.Clone the repository
```bash
git clone <your-repo-url>
cd <your-repo-folder>
```

### 2. Install dependencies
```bash
pip install flask google-genai python-dotenv requests SpeechRecognition pyttsx3 pywin32
```
> `pywin32` is required on Windows for certain speech/audio functionality.

### 3. Add your Gemini API key
Create a file named `.env` in the project root (same folder as `app.py`) with:
```
GEMINI_API_KEY=your_actual_gemini_key_here
```
Get a free key from [Google AI Studio](https://aistudio.google.com/). This file is excluded from git via `.gitignore` — never commit real API keys.

### 4. Run the app
```bash
python app.py
```
The app will start a local Flask server and automatically open `http://127.0.0.1:5000` in your default browser.

5. Use it
Click the Speak button on the page and try commands like:
- "Hello"
- "What time is it?"
- "What's the weather in (any city)?"
- "Search (any) tutorials"
- "What is photosynthesis?" *(routed to Gemini, GK Q&A)*

### Privacy Notes

- Microphone audio is sent to Google's Speech Recognition service for transcription — audio is not stored locally.
- Weather queries send only the city name to Open-Meteo (no personal data).
- General knowledge questions are sent to Google's Gemini API as plain text.
- Your API key is stored locally in `.env` and is never included in the repository.

 

- Custom command support via a config file
- Timed reminders and email integration
