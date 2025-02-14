import can
import struct
from dataclasses import dataclass

@dataclass
class Measurement:
    ID: int
    hex: bytearray
    value: float
    offset: int
    bytes: int
    resolution: float
    data_offset: int

@dataclass
class Data:
    voltage: Measurement
    current: Measurement
    cell_sum: Measurement
    SOC: Measurement
    battery_insulation: Measurement
    load_insulation: Measurement
    battery_SOH: Measurement
    battery_capacity: Measurement
    system_status: Measurement
    system_mode: Measurement
    fault_code: Measurement
    fault_level: Measurement

data = Data(
    voltage=Measurement(0x18F003A0, bytearray(), 0, 0, 2, 0.05, 0),
    current=Measurement(0x18F003A0, bytearray(), 0, 2, 2, 0.05, -1600),
    cell_sum=Measurement(0x18F003A0, bytearray(), 0, 4, 2, 0.05, 0),
    SOC=Measurement(0x18F003A0, bytearray(), 0, 6, 2, 0.1, 0),
    battery_insulation=Measurement(0x18F001A0, bytearray(), 0, 0, 2, 1, 0),
    load_insulation=Measurement(0x18F001A0, bytearray(), 0, 2, 2, 1, 0),
    battery_SOH=Measurement(0x18F001A0, bytearray(), 0, 4, 2, 0.1, 0),
    battery_capacity=Measurement(0x18F001A0, bytearray(), 0, 6, 2, 0.1, 0),
    system_status=Measurement(0x18F000A0, bytearray(), 0, 0, 0, 1, 0),  # 4 bits, stored as 1 byte
    system_mode=Measurement(0x18F000A0, bytearray(), 0, 0, 0, 1, 0),  # 4 bits, stored as 1 byte
    fault_code=Measurement(0x18F000A0, bytearray(), 0, 1, 1, 1, 0),
    fault_level=Measurement(0x18F000A0, bytearray(), 0, 2, 1, 1, 0))

def decode(data_msg, data, msg_id):
    if len(data_msg) < 8:
        return None  # Ensure message has enough data

    for key, measurement in vars(data).items():
        if measurement.ID == msg_id:
            if measurement.bytes == 0:
                data.system_status.value = struct.unpack_from('<B', data_msg, measurement.offset)[0] & 0x0F
                data.system_mode.value = (struct.unpack_from('<B', data_msg, measurement.offset)[0] >> 4) & 0x0F
            if measurement.bytes == 1:
                measurement.value = struct.unpack_from('<B', data_msg, measurement.offset)[0] * measurement.resolution + measurement.data_offset
                measurement.hex = data_msg[measurement.offset:measurement.offset + measurement.bytes]
            elif measurement.bytes == 2:
                measurement.value = struct.unpack_from('<H', data_msg, measurement.offset)[0] * measurement.resolution + measurement.data_offset
                measurement.hex = data_msg[measurement.offset:measurement.offset + measurement.bytes]

    return {True}

def can_listenner(interface='socketcan', channel='can0'):
    try:
        bus = can.interface.Bus(channel=channel, interface=interface)
        print(f"Listening on {channel}...")

        while True:
            print("Waiting")
            msg = bus.recv(timeout=1)  # Wait for a message with timeout

            if msg and len(msg.data) >= 3:
                print(msg.data)
                decoded_data = decode(msg.data, data, msg.arbitration_id)
                '''if decoded_data:
                    if msg.arbitration_id == data.system_status.ID:
                        print(msg.data)
                        print(msg.data.hex())
                    print(str(data.voltage.hex) + "\t\t\t" + str(data.voltage.value))
                    print(str(data.current.hex) + "\t\t\t" + str(data.current.value))
                    print(str(data.system_status.hex) + "\t\t\t" + str(data.system_status.value))
                    print(str(data.battery_capacity.hex) + "\t\t\t" + str(data.battery_capacity.value))
                    print()'''

    except KeyboardInterrupt:
        print("Stopped by user.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        bus.shutdown()

if __name__ == "__main__":
    can_listenner()
