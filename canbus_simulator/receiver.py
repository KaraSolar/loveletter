import time
from can.interfaces.udp_multicast import UdpMulticastBus

def main():
    filters = [
        {"can_id": 0x18F000A0, "can_mask": 0x1FFFFFFF, "extended": True}
    ]
    with UdpMulticastBus(channel=UdpMulticastBus.DEFAULT_GROUP_IPv6, can_filters=filters) as bus2:
        while True:
            try:
                msg=bus2.recv(timeout=0)
                if msg is not None:
                    print(msg)

                    print(msg[2], msg[3])
            except Exception as e:
                print("closing receiver")
                raise e
            else:
                time.sleep(0.9)
if __name__ == "__main__":
    main()