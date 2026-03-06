from models.sea_danger_model import SeaDangerModel
from agents.safety_agent import SafetyAgent
from gps.gps_tracker import GPSTracker


def main():

    print("AI Coastal Guardian System Starting...")

    gps = GPSTracker()
    latitude, longitude = gps.get_location()

    print(f"Boat location: {latitude:.4f}, {longitude:.4f}")

    model = SeaDangerModel()
    model.train()

    agent = SafetyAgent()

    result = model.predict(
        wind_speed=22,
        wave_height=2.7,
        pressure=1001
    )

    agent.evaluate(result)


if __name__ == "__main__":
    main()