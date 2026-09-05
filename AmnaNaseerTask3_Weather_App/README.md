### Advanced Weather Application

A weather app built with the Tkinter library that fetches and displays real-time weather data for a user-specified location using the OpenWeatherMap API and displays predicted weather for 5 days. 

This project was developed as part of my Python Development internship at Oasis Infobyte (OIBSIP).

---
### Features

- **Real-Time Weather Data:** Fetches current temperature, feels-like temperature, humidity, and wind speed.
- **5-Day Forecast:** Displays a visual 5-day weather forecast with dynamic icons.
- **Auto-Location Detection:** Automatically detects the user's city using IP geolocation.
- **Unit Toggle:** Easily switch between Celsius (°C) and Fahrenheit (°F).
- **Dynamic Weather Icons:** Fetches and displays real-time weather condition icons from the API.
- **Robust Error Handling:** Gracefully handles network timeouts, invalid cities, and API errors via GUI popups.

--- 
### Technologies Used

- **Python 3.x**
- **Tkinter** (GUI Framework)
- **Requests** (HTTP library for API calls)
- **Pillow (PIL)** (For handling and displaying weather icons)
- **python-dotenv** (For secure API key management)
- **OpenWeatherMap API** (Free tier for weather data)

  ---
### Project Structure

```text
Task3_Weather_App/
├── gui.py                 # Main GUI application and logic
├── weather_api.py         # API fetching and data parsing
├── requirements.txt       # Python dependencies
├── .env.example           # Template for API key
└── README.md              # Project documentation
├── .env.example           # Template for API key
└── README.md              # Project documentation
