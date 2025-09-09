import gpsd


class GPSQuery:
    def __init__(self):
        gpsd.connect()

    @staticmethod
    def read_and_format_gps_signal():
        packet = gpsd.get_current()
        return {"latitude": packet.lat,
                "longitude": packet.lon,
                "course": packet.track,
                "speed": packet.hspeed,
                "gps_fix": packet.mode,
                "gps_number_of_satellites": packet.sats,
                "altitude": packet.alt}

    @staticmethod
    def disconnect():
        return 0  # gpsd does not have a disconnect method, the socket will be garbage collected.
