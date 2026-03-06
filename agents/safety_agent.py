from communication.distress_signal import DistressSignal


class SafetyAgent:

    def __init__(self):
        self.distress = DistressSignal()

    def evaluate(self, danger_prediction):

        if danger_prediction == 1:
            return self.handle_danger()
        else:
            return self.handle_safe()

    def handle_danger(self):

        print("🚨 Safety Agent: Dangerous sea conditions detected!")
        print("⚠ Recommendation: Return to shore immediately.")

        # simulate distress transmission
        self.distress.send(
            boat_id="FISHER_BOAT_07",
            latitude=8.8932,
            longitude=76.6141
        )

        return "danger"

    def handle_safe(self):

        print("✅ Safety Agent: Sea conditions are safe.")
        print("👍 Fishing operations can continue.")

        return "safe"