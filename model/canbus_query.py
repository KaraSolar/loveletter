import can
import struct


class CanBusQuery:
    def __init__(self, channel="can0"):
        self.channel = channel
        self.filters = [
            {"can_id":0x18F003A0, "can_mask":0x1FFFFFFF, "extended":True},
        ]
        self.bus = can.interface.Bus(channel=self.channel,
                                     interface='socketcan',
                                     can_filters=self.filters)

    @property  # Getter
    def channel(self) -> str:
        """Get the server IP address."""
        return self._channel

    @channel.setter  # Setter
    def channel(self, channel: str) -> None:
        """Set the server IP address.
        Args:
            channel (str): The channel to set.
        Raises:
            ValueError: If the provided channel is not accepted.
        """
        accepted_channels = ("can0", "vcan0")
        if channel not in accepted_channels:
            raise ValueError("Channel not accepted")
        self._channel = channel

    def read_and_format_can_bus_message(self):
        try:
            msg = self.bus.recv(timeout=0.1)  # Small timeout to not block
            if msg:
                msg = self.decoder(msg=msg)
                return msg
            else:
                return {"voltage": None, "current": None, "soc": None,
                        "battery_power": None}

        except:
            pass

    @staticmethod
    def decoder(msg):
        raw_voltage = struct.unpack_from('<H', msg.data, 0)[0]
        raw_current = struct.unpack_from('<H', msg.data, 2)[0]
        # raw_cell_sum = struct.unpack_from('<H', msg.data, 4)[0]
        raw_soc = struct.unpack_from('<H', msg.data, 6)[0]
        voltage = (raw_voltage * 0.05) + 0
        current = (raw_current * 0.05) - 1600
        # cell_sum = (raw_cell_sum * 0.05) + 0
        soc = (raw_soc * 0.1) + 0
        return {"voltage": voltage, "current": current, "soc": soc,
                "battery_power": voltage * current}

    def disconnect(self):
        self.bus.shutdown()
