import tkinter as tk
from tkinter import ttk, messagebox
import requests
import os
from dotenv import load_dotenv
from PIL import Image, ImageTk
import io
from datetime import datetime

# Load environment variables
load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
FORECAST_URL = "https://api.openweathermap.org/data/2.5/forecast"
GEO_URL = "http://api.openweathermap.org/geo/1.0/direct"

class WeatherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Weather App")
        self.root.geometry("1000x850")  # Larger window
        self.root.configure(bg='#1e1e2e')
        
        self.unit = "metric"
        self.unit_symbol = "°C"
        self.current_city = ""
        
        # Create main canvas with scrollbar
        self.main_canvas = tk.Canvas(root, bg='#1e1e2e', highlightthickness=0)
        scrollbar = ttk.Scrollbar(root, orient="vertical", command=self.main_canvas.yview)
        
        self.scrollable_frame = tk.Frame(self.main_canvas, bg='#1e1e2e')
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.main_canvas.configure(scrollregion=self.main_canvas.bbox("all"))
        )
        
        self.main_canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.main_canvas.configure(yscrollcommand=scrollbar.set)
        
        self.main_canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        self.create_widgets()
        
    def create_widgets(self):
        # Header
        header_frame = tk.Frame(self.scrollable_frame, bg='#1e1e2e')
        header_frame.pack(pady=20, padx=20)
        
        title_label = tk.Label(
            header_frame, 
            text="🌤️ Advanced Weather App", 
            font=("Helvetica", 24, "bold"),
            bg='#1e1e2e', 
            fg='#ffffff'
        )
        title_label.pack()
        
        # Search Frame
        search_frame = tk.Frame(self.scrollable_frame, bg='#1e1e2e')
        search_frame.pack(pady=10, padx=20)
        
        self.city_entry = tk.Entry(
            search_frame, 
            font=("Helvetica", 14),
            width=30,
            bg='#2a2a3e',
            fg='#ffffff',
            insertbackground='white',
            relief=tk.FLAT
        )
        self.city_entry.pack(side=tk.LEFT, padx=10, ipady=8)
        self.city_entry.bind('<Return>', lambda e: self.get_weather())
        
        search_btn = tk.Button(
            search_frame,
            text="🔍 Get Weather",
            font=("Helvetica", 12, "bold"),
            bg='#4a9eff',
            fg='white',
            relief=tk.FLAT,
            cursor="hand2",
            command=self.get_weather,
            padx=20,
            pady=8
        )
        search_btn.pack(side=tk.LEFT, padx=10)
        
        # Unit Toggle & Auto Detect
        unit_frame = tk.Frame(self.scrollable_frame, bg='#1e1e2e')
        unit_frame.pack(pady=10, padx=20)
        
        self.unit_btn = tk.Button(
            unit_frame,
            text="Switch to °F",
            font=("Helvetica", 11),
            bg='#5a5a7e',
            fg='white',
            relief=tk.FLAT,
            cursor="hand2",
            command=self.toggle_unit,
            padx=15,
            pady=5
        )
        self.unit_btn.pack(side=tk.LEFT, padx=10)

        auto_btn = tk.Button(
            unit_frame,
            text="📍 Detect My Location",
            font=("Helvetica", 11),
            bg='#5a5a7e',
            fg='white',
            relief=tk.FLAT,
            cursor="hand2",
            command=self.auto_detect_location,
            padx=15,
            pady=5
        )
        auto_btn.pack(side=tk.LEFT, padx=10)
        
        # Current Weather Frame
        self.current_frame = tk.LabelFrame(
            self.scrollable_frame,
            text="Current Weather",
            font=("Helvetica", 14, "bold"),
            bg='#2a2a3e',
            fg='#ffffff',
            padx=20,
            pady=20
        )
        self.current_frame.pack(fill=tk.BOTH, expand=True, pady=10, padx=20)
        
        self.weather_info_label = tk.Label(
            self.current_frame,
            text="Enter a city name and click 'Get Weather'",
            font=("Helvetica", 12),
            bg='#2a2a3e',
            fg='#aaaaaa'
        )
        self.weather_info_label.pack()
        
        # Forecast Frame
        self.forecast_frame = tk.LabelFrame(
            self.scrollable_frame,
            text="5-Day Forecast",
            font=("Helvetica", 14, "bold"),
            bg='#2a2a3e',
            fg='#ffffff',
            padx=20,
            pady=20
        )
        self.forecast_frame.pack(fill=tk.BOTH, expand=True, pady=10, padx=20)
        
        self.forecast_container = tk.Frame(self.forecast_frame, bg='#2a2a3e')
        self.forecast_container.pack(fill=tk.BOTH, expand=True)
        
        self.forecast_label = tk.Label(
            self.forecast_container,
            text="Forecast will appear here after you search for a city",
            font=("Helvetica", 11),
            bg='#2a2a3e',
            fg='#aaaaaa'
        )
        self.forecast_label.pack(pady=20)
        
    def toggle_unit(self):
        if self.unit == "metric":
            self.unit = "imperial"
            self.unit_symbol = "°F"
            self.unit_btn.config(text="Switch to °C")
        else:
            self.unit = "metric"
            self.unit_symbol = "°C"
            self.unit_btn.config(text="Switch to °F")
        
        if self.current_city:
            self.get_weather()
    
    def auto_detect_location(self):
        try:
            response = requests.get("http://ip-api.com/json/", timeout=5)
            data = response.json()
            
            if data.get('status') == 'success' and 'city' in data:
                city = data['city']
                self.city_entry.delete(0, tk.END)
                self.city_entry.insert(0, city)
                
                messagebox.showinfo(
                    "Location Detected", 
                    f"Detected location: {city}\n\nPlease verify this is correct, then click 'Get Weather'!"
                )
            else:
                messagebox.showwarning("Location Detection", "Could not detect your location")
        except Exception as e:
            messagebox.showerror("Error", f"Location detection failed: {str(e)}")
    
    def get_weather(self):
        city = self.city_entry.get().strip()
        
        if not city:
            messagebox.showwarning("Input Error", "Please enter a city name!")
            return
        
        self.current_city = city
        
        try:
            params = {
                "q": city,
                "appid": API_KEY,
                "units": self.unit
            }
            
            response = requests.get(BASE_URL, params=params, timeout=10)
            
            if response.status_code == 404:
                messagebox.showerror("Error", "City not found! Please check the spelling.")
                return
            elif response.status_code == 401:
                messagebox.showerror("Error", "Invalid API Key!")
                return
            elif response.status_code != 200:
                messagebox.showerror("Error", f"API Error: {response.status_code}")
                return
            
            data = response.json()
            self.display_current_weather(data)
            self.get_forecast(city)
            
        except requests.exceptions.Timeout:
            messagebox.showerror("Error", "Request timed out. Check internet connection.")
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"Network error: {str(e)}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
    
    def display_current_weather(self, data):
        for widget in self.current_frame.winfo_children():
            widget.destroy()
        
        city_name = data['name']
        country = data['sys']['country']
        temp = data['main']['temp']
        feels_like = data['main']['feels_like']
        humidity = data['main']['humidity']
        description = data['weather'][0]['description'].title()
        wind_speed = data['wind']['speed']
        icon_code = data['weather'][0]['icon']
        
        top_frame = tk.Frame(self.current_frame, bg='#2a2a3e')
        top_frame.pack(fill=tk.BOTH, expand=True)
        
        left_frame = tk.Frame(top_frame, bg='#2a2a3e')
        left_frame.pack(side=tk.LEFT, padx=20)
        
        try:
            icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
            icon_response = requests.get(icon_url, timeout=5)
            if icon_response.status_code == 200:
                icon_image = Image.open(io.BytesIO(icon_response.content))
                icon_photo = ImageTk.PhotoImage(icon_image)
                
                icon_label = tk.Label(left_frame, image=icon_photo, bg='#2a2a3e')
                icon_label.image = icon_photo
                icon_label.pack()
        except:
            icon_label = tk.Label(left_frame, text="🌤️", font=("Helvetica", 72), bg='#2a2a3e')
            icon_label.pack()
        
        right_frame = tk.Frame(top_frame, bg='#2a2a3e')
        right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20)
        
        city_label = tk.Label(right_frame, text=f"{city_name}, {country}", font=("Helvetica", 20, "bold"), bg='#2a2a3e', fg='#ffffff')
        city_label.pack(anchor='w', pady=(0, 10))
        
        temp_label = tk.Label(right_frame, text=f"{temp:.1f}{self.unit_symbol}", font=("Helvetica", 48, "bold"), bg='#2a2a3e', fg='#4a9eff')
        temp_label.pack(anchor='w')
        
        desc_label = tk.Label(right_frame, text=description, font=("Helvetica", 16), bg='#2a2a3e', fg='#cccccc')
        desc_label.pack(anchor='w', pady=(5, 15))
        
        details_frame = tk.Frame(right_frame, bg='#2a2a3e')
        details_frame.pack(fill=tk.BOTH, expand=True)
        
        details = [
            ("Feels Like:", f"{feels_like:.1f}{self.unit_symbol}"),
            ("Humidity:", f"{humidity}%"),
            ("Wind Speed:", f"{wind_speed} m/s"),
        ]
        
        for i, (label, value) in enumerate(details):
            lbl = tk.Label(details_frame, text=label, font=("Helvetica", 12), bg='#2a2a3e', fg='#aaaaaa')
            lbl.grid(row=i, column=0, sticky='w', pady=5, padx=(0, 20))
            
            val = tk.Label(details_frame, text=value, font=("Helvetica", 12, "bold"), bg='#2a2a3e', fg='#ffffff')
            val.grid(row=i, column=1, sticky='w', pady=5)
    
    def get_forecast(self, city):
        try:
            geo_params = {"q": city, "appid": API_KEY, "limit": 1}
            geo_response = requests.get(GEO_URL, params=geo_params, timeout=10)
            if geo_response.status_code != 200: return
            
            geo_data = geo_response.json()
            if not geo_data: return
            
            lat = geo_data[0]['lat']
            lon = geo_data[0]['lon']
            
            forecast_params = {"lat": lat, "lon": lon, "appid": API_KEY, "units": self.unit, "cnt": 40}
            response = requests.get(FORECAST_URL, params=forecast_params, timeout=10)
            
            if response.status_code != 200: return
            
            forecast_data = response.json()
            self.display_forecast(forecast_data['list'])
            
        except Exception as e:
            print(f"Forecast error: {e}")
    
    def display_forecast(self, forecast_list):
        # Clear previous forecast
        for widget in self.forecast_container.winfo_children():
            widget.destroy()
        
        # Group forecasts by day
        daily_forecasts = {}
        
        for item in forecast_list:
            dt = datetime.fromtimestamp(item['dt'])
            date_str = dt.strftime('%Y-%m-%d')
            hour = dt.hour
            
            if date_str not in daily_forecasts or abs(hour - 12) < abs(daily_forecasts[date_str]['hour'] - 12):
                daily_forecasts[date_str] = {
                    'temp': item['main']['temp'],
                    'description': item['weather'][0]['description'].title(),
                    'icon': item['weather'][0]['icon'],
                    'hour': hour,
                    'dt': dt
                }
        
        # Create cards frame
        cards_frame = tk.Frame(self.forecast_container, bg='#2a2a3e')
        cards_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Display daily forecasts in a horizontal row
        for i, (date_str, data) in enumerate(sorted(daily_forecasts.items())[:5]):
            day_frame = tk.Frame(cards_frame, bg='#3a3a5e', padx=15, pady=15, relief=tk.RAISED, bd=2)
            day_frame.grid(row=0, column=i, padx=10, pady=10, sticky="nsew")
            cards_frame.columnconfigure(i, weight=1)
            
            # Date
            date_obj = datetime.strptime(date_str, '%Y-%m-%d')
            day_name = date_obj.strftime('%A')[:3]
            date_display = date_obj.strftime('%b %d')
            
            date_label = tk.Label(day_frame, text=f"{day_name}\n{date_display}", font=("Helvetica", 11, "bold"), bg='#3a3a5e', fg='#ffffff')
            date_label.pack(pady=(0, 10))
            
            # Icon
            try:
                icon_url = f"http://openweathermap.org/img/wn/{data['icon']}@2x.png"
                icon_response = requests.get(icon_url, timeout=5)
                if icon_response.status_code == 200:
                    icon_image = Image.open(io.BytesIO(icon_response.content))
                    icon_image = icon_image.resize((60, 60), Image.Resampling.LANCZOS)
                    icon_photo = ImageTk.PhotoImage(icon_image)
                    
                    icon_label = tk.Label(day_frame, image=icon_photo, bg='#3a3a5e')
                    icon_label.image = icon_photo
                    icon_label.pack()
            except:
                icon_label = tk.Label(day_frame, text="🌤️", font=("Helvetica", 32), bg='#3a3a5e')
                icon_label.pack()
            
            # Temperature
            temp_label = tk.Label(day_frame, text=f"{data['temp']:.0f}{self.unit_symbol}", font=("Helvetica", 16, "bold"), bg='#3a3a5e', fg='#4a9eff')
            temp_label.pack(pady=5)
            
            # Description
            desc_label = tk.Label(day_frame, text=data['description'], font=("Helvetica", 9), bg='#3a3a5e', fg='#cccccc', wraplength=120)
            desc_label.pack()

def main():
    root = tk.Tk()
    app = WeatherApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()