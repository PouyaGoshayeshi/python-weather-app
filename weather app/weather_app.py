import tkinter as tk
from tkinter import messagebox
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
from datetime import datetime
import requests
import pytz


def get_weather():
    try:
        # city
        city = textfield.get().strip()

        if not city:
            messagebox.showerror("Weather App", "Please enter a city name.")
            return

        # location
        geolocator = Nominatim(user_agent="weather_app")
        location = geolocator.geocode(city)

        if location is None:
            messagebox.showerror("Weather App", "City not found.")
            return

        lat = location.latitude
        lng = location.longitude

        # timezone
        timezone_finder = TimezoneFinder()
        timezone_name = timezone_finder.timezone_at(lng=lng, lat=lat)

        if timezone_name:
            city_label.config(
                text=timezone_name.split("/")[-1].replace("_", " ")
            )

            home = pytz.timezone(timezone_name)
            local_time = datetime.now(home)
            current_time = local_time.strftime("%I:%M %p")

            clock_label.config(text=current_time)
            time_label.config(text="LOCAL TIME")
        else:
            city_label.config(text=city.title())
            clock_label.config(text="")
            time_label.config(text="")

        # weather
        api_key = "256e9e4c7dda7ac72318dc0f1aafbd28"

        api = (
            "https://api.openweathermap.org/data/2.5/weather"
            f"?lat={lat}&lon={lng}&appid={api_key}&units=metric"
        )

        response = requests.get(api, timeout=10)
        response.raise_for_status()
        json_data = response.json()

        condition = json_data["weather"][0]["main"]
        description = json_data["weather"][0]["description"]

        temp = round(json_data["main"]["temp"])
        feels_like = round(json_data["main"]["feels_like"])

        pressure = json_data["main"]["pressure"]
        humidity = json_data["main"]["humidity"]
        wind = json_data["wind"]["speed"]

        # update GUI
        temp_label.config(text=f"{temp}°C")

        condition_label.config(
            text=f"{condition} | Feels like {feels_like}°C"
        )

        wind_label.config(text=f"{wind} m/s")
        humidity_label.config(text=f"{humidity}%")
        description_label.config(text=description.title())
        pressure_label.config(text=f"{pressure} hPa")

    except requests.RequestException as error:
        print(error)
        messagebox.showerror(
            "Weather App",
            "Could not connect to the weather service."
        )

    except Exception as error:
        print(error)
        messagebox.showerror(
            "Weather App",
            "Something went wrong."
        )


root = tk.Tk()

root.title("Weather App")
root.geometry("900x500+300+200")
root.resizable(False, False)


# Search box
search_image = tk.PhotoImage(file="search.png")

search_image_label = tk.Label(
    root,
    image=search_image
)
search_image_label.pack(
    pady=20,
    side=tk.TOP
)


textfield = tk.Entry(
    root,
    justify="center",
    width=17,
    font=("Poppins", 25, "bold"),
    bg="#404040",
    fg="white",
    border=0
)

textfield.place(
    x=280,
    y=40
)


# Search icon
search_icon = tk.PhotoImage(
    file="search_icon.png"
)

search_icon_button = tk.Button(
    root,
    image=search_icon,
    border=0,
    cursor="hand2",
    bg="#404040",
    activebackground="#404040",
    command=get_weather
)

search_icon_button.place(
    x=590,
    y=34
)


# Press Enter to search
textfield.bind(
    "<Return>",
    lambda event: get_weather()
)


# Logo
logo_image = tk.PhotoImage(
    file="logo.png"
)

logo_label = tk.Label(
    root,
    image=logo_image
)

logo_label.pack(
    side=tk.TOP
)


# Bottom box
frame_image = tk.PhotoImage(
    file="box.png"
)

frame_label = tk.Label(
    root,
    image=frame_image
)

frame_label.pack(
    pady=10,
    side=tk.BOTTOM
)


# City name
city_label = tk.Label(
    root,
    font=("Arial", 40, "bold"),
    fg="#e355cd"
)

city_label.place(
    x=120,
    y=160
)


# Local time title
time_label = tk.Label(
    root,
    font=("Arial", 20, "bold"),
    fg="#4b4bcc"
)

time_label.place(
    x=120,
    y=230
)


# Clock
clock_label = tk.Label(
    root,
    font=("Helvetica", 20),
    fg="#4b4bcc"
)

clock_label.place(
    x=120,
    y=270
)


# Bottom titles
label1 = tk.Label(
    root,
    text="WIND",
    font=("Helvetica", 15, "bold"),
    fg="white",
    bg="#1ab5ef"
)

label1.place(
    x=120,
    y=400
)


label2 = tk.Label(
    root,
    text="HUMIDITY",
    font=("Helvetica", 15, "bold"),
    fg="white",
    bg="#1ab5ef"
)

label2.place(
    x=280,
    y=400
)


label3 = tk.Label(
    root,
    text="DESCRIPTION",
    font=("Helvetica", 15, "bold"),
    fg="white",
    bg="#1ab5ef"
)

label3.place(
    x=450,
    y=400
)


label4 = tk.Label(
    root,
    text="PRESSURE",
    font=("Helvetica", 15, "bold"),
    fg="white",
    bg="#1ab5ef"
)

label4.place(
    x=670,
    y=400
)


# Temperature
temp_label = tk.Label(
    root,
    font=("Arial", 25, "bold"),
    fg="#e355cd"
)

temp_label.place(
    x=590,
    y=170
)


# Weather condition
condition_label = tk.Label(
    root,
    font=("Arial", 15, "bold"),
    fg="#4b4bcc"
)

condition_label.place(
    x=590,
    y=270
)


# Wind value
wind_label = tk.Label(
    root,
    text="...",
    font=("Arial", 18, "bold"),
    bg="#1ab5ef",
    fg="#404040"
)

wind_label.place(
    x=120,
    y=430
)


# Humidity value
humidity_label = tk.Label(
    root,
    text="...",
    font=("Arial", 18, "bold"),
    bg="#1ab5ef",
    fg="#404040"
)

humidity_label.place(
    x=280,
    y=430
)


# Description value
description_label = tk.Label(
    root,
    text="...",
    font=("Arial", 14, "bold"),
    bg="#1ab5ef",
    fg="#404040"
)

description_label.place(
    x=450,
    y=430
)


# Pressure value
pressure_label = tk.Label(
    root,
    text="...",
    font=("Arial", 18, "bold"),
    bg="#1ab5ef",
    fg="#404040"
)

pressure_label.place(
    x=670,
    y=430
)


root.mainloop()
