import os
from dotenv import load_dotenv
import requests

load_dotenv()

class WeatherAPI:

    def __init__(self, api_key):
        self.api_key = api_key

    def get_weather(self, latitude, longitude):
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={self.api_key}&units=metric"

        response = requests.get(url)

        if response.status_code != 200:
            print("Status Code:", response.status_code)
            print("Response:", response.text)
            return None

        data = response.json()

        weather_data = {
            "temperature": data["main"]["temp"],
            "pressure": data["main"]["pressure"],
            "wind_speed": data["wind"]["speed"]
        }

        return weather_data
    
# TEST SECTION
if __name__ == "__main__":

    API_KEY = os.getenv("OPENWEATHER_API_KEY")

    weather = WeatherAPI(API_KEY)

    data = weather.get_weather(8.89, 76.59)

    print(data)