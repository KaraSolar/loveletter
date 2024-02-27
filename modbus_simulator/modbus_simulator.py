from pymodbus.server.sync import StartTcpServer


class ModbusSimulator:
    def __init__(self):
        # Initialize registers with random integers
        self.start_server()

    def start_server(self):
        # Start Modbus TCP server
        StartTcpServer(address=("127.0.0.1", 12345))

if __name__ == "__main__":
    simulator = ModbusSimulator()
    simulator.start_server()

