class MonitoringAgent:

    def observe(self, gps_tracker, weather_api):

        latitude, longitude = gps_tracker.get_location()

        weather_data = weather_api.get_weather(latitude, longitude)

        return latitude, longitude, weather_data