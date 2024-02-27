'''
TO DO:
1. ip finder
pending el unit_id para gps.
Esta libreria no se reconecta automaticamente, si no encuentra coneccion chao lola

'''

from pymodbus.exceptions import ModbusException, ModbusIOException
from pymodbus.client.sync import ModbusTcpClient


class ModbusQuery:
    def __init__(self, server_ip="127.0.0.1", server_port=12345):
        self.server_ip = server_ip
        self.server_port = server_port
        self.client = ModbusTcpClient(self.server_ip, port=self.server_port)
        self.client.connect()
        self.register_values = None

    def read_registers(self, address, count, unit):
        try:
            response =  self.client.read_holding_registers(address=address, count=count, unit=unit)
            response = response.registers
        except (ModbusIOException, ModbusException, AttributeError) as exe:
            raise exe
        else:
            return response

    def read_telemetry_registers(self) -> list:
        battery_regs = self.read_registers(address=840, count=4, unit=100)  # 840 to 843
        solar_regs = self.read_registers(address=850, count=2, unit=100)  # 850 to 851
        georef_regs = self.read_registers(address=2800, count=10, unit=1)  # 2800 to 2809
        self.register_values = battery_regs + solar_regs + georef_regs

    def register_values_formatting(self):
        if self.register_values != 12:
            raise ValueError("Not a read_telemetry_registers list")
        self.verify_negative_values()
        self.set_scaling()

    def set_scaling(self)->None:
        for index in (0,1,5):
            try:
                self.register_values[index] = self.register_values[index] / 10
            except TypeError:
                pass
        try:
            self.register_values[11] = self.register_values[11] / 100
        except TypeError:
            pass

    def verify_negative_values(self)->None:
        for index in (1,2,5):
            try:
                if self.register_values[index] >= 32768:
                    self.register_values[index] = self.register_values[index] - 65536
            except TypeError:
                pass

    def disconnect(self):
        self.client.close()
        return 0
