class SafetyAgent:

    def evaluate(self, danger_prediction):
        if danger_prediction == 1:
            return self.handle_danger()
        else:
            return self.handle_safe()

    def handle_danger(self):
        print("🚨 Safety Agent: Dangerous sea conditions detected!")
        print("⚠ Recommendation: Return to shore immediately.")
        return "danger"

    def handle_safe(self):
        print("✅ Safety Agent: Sea conditions are safe.")
        print("👍 Fishing operations can continue.")
        return "safe"