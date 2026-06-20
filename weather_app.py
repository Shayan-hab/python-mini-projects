import requests
import tkinter as tk
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

# Constants
API_KEY = '96b1081cef658d27aba8574b6c8305aa'
BASE_URL = 'https://api.openweathermap.org/data/2.5/weather'
FORECAST_URL = 'https://api.openweathermap.org/data/2.5/forecast'
GROUP_URL = 'https://api.openweathermap.org/data/2.5/group'

# Fetch weather for a specific city
def fetch_weather():
    city = city_name.get()
    if not city:
        messagebox.showerror("Error", "Please enter a city name.")
        return

    try:
        response = requests.get(BASE_URL, params={
            'q': city,
            'appid': API_KEY,
            'units': 'metric'
        })
        response.raise_for_status()
        data = response.json()
        display_weather(data)
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"Unable to fetch data: {e}")

# Display weather details in the GUI
def display_weather(data):
    temperature = data['main']['temp']
    humidity = data['main']['humidity']
    pressure = data['main']['pressure']
    description = data['weather'][0]['description']

    result.set(f"Temperature: {temperature}°C\n"
               f"Humidity: {humidity}%\n"
               f"Pressure: {pressure} hPa\n"
               f"Description: {description.capitalize()}")

# Fetch and display 10 coldest cities
def plot_coldest_cities():
    city_ids = [1174872, 1172451, 1162015, 1167528, 1168197, 1169825, 1177446, 1176615, 1170395, 1180809]  # IDs of major Pakistani cities

    try:
        response = requests.get(GROUP_URL, params={
            'id': ','.join(map(str, city_ids)),
            'appid': API_KEY,
            'units': 'metric'
        })
        response.raise_for_status()
        data = response.json()

        temps = [(city['name'], city['main']['temp']) for city in data['list']]
        temps = sorted(temps, key=lambda x: x[1])[:10]

        # Plot bar chart
        cities = [item[0] for item in temps]
        temperatures = [item[1] for item in temps]
        fig, ax = plt.subplots()
        ax.bar(cities, temperatures)
        ax.set_title("10 Coldest Cities in Pakistan")
        ax.set_ylabel("Temperature (°C)")
        ax.set_xlabel("Cities")

        # Embed chart in GUI
        display_chart(fig)
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"Unable to fetch data: {e}")

# Embed Matplotlib chart in Tkinter
def display_chart(fig):
    canvas = FigureCanvasTkAgg(fig, master=app)
    canvas.draw()
    canvas.get_tk_widget().pack(pady=10)

# GUI Setup
app = tk.Tk()
app.title("Weather App")

# Input for city name
tk.Label(app, text="Enter City Name:").pack(pady=5)
city_name = tk.StringVar()
tk.Entry(app, textvariable=city_name).pack(pady=5)

# Buttons
tk.Button(app, text="Get Weather", command=fetch_weather).pack(pady=5)
tk.Button(app, text="Show Coldest Cities", command=plot_coldest_cities).pack(pady=5)

# Weather result
result = tk.StringVar()
tk.Label(app, textvariable=result, justify="left").pack(pady=10)

app.mainloop()

