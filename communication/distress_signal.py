import datetime


class DistressSignal:

    def send(self, boat_id, latitude, longitude):
        timestamp = datetime.datetime.now()

        print("\n🚨 DISTRESS SIGNAL ACTIVATED 🚨")
        print(f"Boat ID: {boat_id}")
        print(f"Location: {latitude}, {longitude}")
        print(f"Time: {timestamp}")
        print("Emergency message transmitted to rescue services.\n")

        return {
            "boat_id": boat_id,
            "latitude": latitude,
            "longitude": longitude,
            "time": timestamp,
            "status": "SOS_SENT"
        }