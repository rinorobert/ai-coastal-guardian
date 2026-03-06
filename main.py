from models.sea_danger_model import SeaDangerModel
from agents.safety_agent import SafetyAgent
from gps.gps_tracker import GPSTracker
from data.weather_api import WeatherAPI
from utils.risk_engine import RiskEngine
from agents.monitoring_agent import MonitoringAgent
from agents.risk_agent import RiskAgent
from datetime import datetime

import os
import time
from dotenv import load_dotenv

load_dotenv()


def main():

    print("AI Coastal Guardian System Starting...\n")

    # Initialize core modules
    model = SeaDangerModel()
    model.train()

    agent = SafetyAgent()
    gps = GPSTracker()
    risk_engine = RiskEngine()
    monitor = MonitoringAgent()

    API_KEY = os.getenv("OPENWEATHER_API_KEY")
    weather_api = WeatherAPI(API_KEY)

    while True:
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"\n[{timestamp}] --- Monitoring Sea Conditions ---\n")

        # 1️⃣ Monitoring Agent observes environment
        latitude, longitude, weather_data = monitor.observe(gps, weather_api)

        print("Boat Location:")
        print(f"Latitude: {latitude:.4f}")
        print(f"Longitude: {longitude:.4f}")

        if weather_data is None:
            print("Weather data unavailable.")
            time.sleep(60)
            continue

        print("\nWeather Conditions:")
        print(f"Temperature: {weather_data['temperature']} °C")
        print(f"Pressure: {weather_data['pressure']} hPa")
        print(f"Wind Speed: {weather_data['wind_speed']} m/s")

        # Estimate wave height using wind speed
        wave_height = weather_data["wind_speed"] * 0.1

        # 2️⃣ AI Prediction , Risk level and Explantion
        risk_agent = RiskAgent()
        prediction, explanation, risk_level = risk_agent.assess(
            model,
            risk_engine,
            weather_data,
            wave_height
        )

        print()
        print("Risk Level:", risk_level)
        print()

        print("AI Explanation:")
        for feature, score in explanation.items():
            print(f"{feature}: influence score {score}")

        print()

        # 3️⃣ Safety Agent Decision
        if risk_level == "HIGH":
            agent.evaluate(1)

        elif risk_level == "MEDIUM":
            print("⚠ Moderate sea conditions detected.")
            print("Please remain cautious while fishing.")

        else:
            agent.evaluate(0)

        # 4️⃣ Wait before next monitoring cycle
        print("\nNext check in 60 seconds...\n")

        time.sleep(60)


if __name__ == "__main__":
    main()