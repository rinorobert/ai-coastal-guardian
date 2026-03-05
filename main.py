from models.sea_danger_model import SeaDangerModel
from agents.safety_agent import SafetyAgent


def main():
    print("AI Coastal Guardian System Starting...")

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