class RiskAgent:

    def assess(self, model, risk_engine, weather_data,wave_height):

        # AI prediction
        prediction = model.predict(
            wind_speed=weather_data["wind_speed"],
            wave_height=wave_height,
            pressure=weather_data["pressure"]
        )

        # Explainable AI
        explanation = model.explain_prediction()

        # Risk evaluation
        risk_level = risk_engine.evaluate(weather_data, prediction)

        return prediction, explanation, risk_level