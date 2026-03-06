import pandas as pd
from sklearn.ensemble import RandomForestClassifier


class SeaDangerModel:
    def __init__(self):
        self.model = RandomForestClassifier()

    def train(self):
        # Example training data
        data = {
            "wind_speed": [5, 10, 20, 15, 30],
            "wave_height": [0.5, 1.2, 2.5, 1.8, 3.5],
            "pressure": [1012, 1008, 1002, 1005, 998],
            "danger": [0, 0, 1, 0, 1]
        }

        df = pd.DataFrame(data)

        X = df[["wind_speed", "wave_height", "pressure"]]
        y = df["danger"]

        self.model.fit(X, y)

    def predict(self, wind_speed, wave_height, pressure):
        input_data = pd.DataFrame([{
            "wind_speed": wind_speed,
            "wave_height": wave_height,
            "pressure": pressure
        }])
        prediction = self.model.predict(input_data)
        return prediction[0]
    
    def explain_prediction(self):

        importance = self.model.feature_importances_

        features = ["wind_speed", "wave_height", "pressure"]

        explanation = {}

        for feature, value in zip(features, importance):
            explanation[feature] = round(value, 3)

        return explanation