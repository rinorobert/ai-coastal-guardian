import random


class GPSTracker:

    def get_location(self):
        """
        Simulate boat GPS coordinates near the Kerala coast
        """

        latitude = 8.89 + random.uniform(-0.05, 0.05)
        longitude = 76.59 + random.uniform(-0.05, 0.05)

        return latitude, longitude