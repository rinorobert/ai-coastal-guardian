class RiskEngine:

    def evaluate(self, weather_data, ai_prediction):

        wind = weather_data["wind_speed"]
        pressure = weather_data["pressure"]

        # --- Rule Based Safety Checks ---
        if wind > 12:
            return "HIGH"

        if wind > 8:
            return "MEDIUM"

        if pressure < 1000:
            return "MEDIUM"

        # --- AI Prediction Check ---
        if ai_prediction == 1:
            return "HIGH"

        return "LOW"