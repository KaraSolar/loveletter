# import gpsd
import random


class GPSQuery:
    def __init__(self):
        pass
        # gpsd.connect()

    @staticmethod
    def read_and_format_gps_signal():
        return {"latitude": 0, "longitude": 0, "course": random.randint(0, 359),
                "speed": random.uniform(0, 5.55), "gps_fix": 10,
                "gps_number_of_satellites": 10, "altitude": 2800}

    @staticmethod
    def disconnect():
        return 0
