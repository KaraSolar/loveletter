import struct
import time
import can
from can.interfaces.udp_multicast import UdpMulticastBus


def main():
    with can.Bus(channel=UdpMulticastBus.DEFAULT_GROUP_IPv6, interface='udp_multicast') as bus1:
        print("sim starting")
        can_data_payload = standard_message()
        bmu_system_status_1_message = bmu_system_status_1()
        try:
            while True:
                counter = 0
                if counter % 10 == 0:
                    message_1 = can.Message(arbitration_id=0x18F001A0,
                                          is_extended_id=True,
                                          data=bmu_system_status_1_message,
                                          dlc=8)
                    bus1.send(message_1)
                message = can.Message(arbitration_id=0x18F000A0,
                                      is_extended_id=True,
                                      data=can_data_payload,
                                      dlc=8)
                bus1.send(message)
                time.sleep(0.1)
                counter += 1
        except:
            print("sim closing...")


def standard_message():
    system_operating_status = 3
    system_operating_mode = 0
    fault_code = 12
    fault_level = 1
    can_data_payload = [0] * 8
    can_data_payload[0] = (system_operating_status & 0xF) | ((system_operating_mode & 0xF) << 4)
    can_data_payload[1] = fault_code & 0xFF
    can_data_payload[2] = fault_level & 0xFF
    return can_data_payload


def bmu_system_status_1():
    battery_insulation_resistance = 500
    load_insulation_resistance = 750
    battery_total_soh = 85.5
    battery_nominal_capacity = 250.0

    battery_total_soh_raw = int(battery_total_soh / 0.1)
    battery_nominal_capacity_raw = int(battery_nominal_capacity / 0.1)

    can_data_payload = [0] * 8

    resistance_bytes = struct.pack('<H', battery_insulation_resistance)

    can_data_payload[0] = resistance_bytes[0]
    can_data_payload[1] = resistance_bytes[1]

    load_resistance_bytes = struct.pack('<H', load_insulation_resistance)
    can_data_payload[0] = load_resistance_bytes[0]
    can_data_payload[3] = load_resistance_bytes[1]

    soh_bytes = struct.pack('<H', battery_total_soh_raw)
    can_data_payload[4] = soh_bytes[0]
    can_data_payload[5] = soh_bytes[1]

    capacity_bytes = struct.pack('<H', battery_nominal_capacity_raw)
    can_data_payload[6] = capacity_bytes[0]
    can_data_payload[7] = capacity_bytes[1]

    return can_data_payload


if __name__ == "__main__":
    main()