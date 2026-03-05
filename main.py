from models.sea_danger_model import SeaDangerModel


def main():
    print("AI Coastal Guardian System Starting...")

    model = SeaDangerModel()
    model.train()

    result = model.predict(
        wind_speed=22,
        wave_height=2.7,
        pressure=1001
    )

    if result == 1:
        print("⚠ Dangerous sea conditions detected!")
    else:
        print("✅ Sea conditions are safe.")


if __name__ == "__main__":
    main()