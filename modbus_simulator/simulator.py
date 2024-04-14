from pyModbusTCP.server import ModbusServer, DataBank
from random import randint

class piDataBank(DataBank):
    def __init__(self):
        super().__init__(h_regs_size=3000) # max register used for the sim is 2808 so 3000 rounded.
        self.registers = {
            "battery_voltage": 0,
            "battery_power": 0,
            "battery_state_of_charge": 100,
            "battery_current": 0,
            "pv_dc_coupled": 0,
            "pv_dc_coupled_current": 0,
            "speed": 0,
            "Latitude": 0,
            "Latitude2": 0,
            "Longitude": 0,
            "Longitude2": 0,
            "GPS fix": 0,
            "GPS number of satellites": 0,
            "Course": 0,
            "Altitude": 0}

    def get_holding_registers(self, address, number=1, srv_info=None):
        self._h_regs[840] = self.registers["battery_voltage"]
        self._h_regs[841] = self.registers["battery_current"]
        self._h_regs[842] = self.registers["battery_power"]
        self._h_regs[843] = self.registers["battery_state_of_charge"]
        self._h_regs[850] = self.registers["pv_dc_coupled"]
        self._h_regs[851] = self.registers["pv_dc_coupled_current"]
        self._h_regs[2805] = self.registers["speed"]
        self._h_regs[2800] = self.registers["Latitude"]
        self._h_regs[2801] = self.registers["Latitude2"]
        self._h_regs[2802] = self.registers["Longitude"]
        self._h_regs[2803] = self.registers["Longitude2"]
        self._h_regs[2804] = self.registers["Course"]
        self._h_regs[2806] = self.registers["GPS fix"]
        self._h_regs[2807] = self.registers["GPS number of satellites"]
        self._h_regs[2808] = self.registers["Altitude"]

        self.increasers(0.2, 0.05, 0.1, 0.1, 1)

        try:
            return [round(self._h_regs[i]) for i in range(address, address + number)]
        except KeyError:
            return

    def increasers(self, battery_power_i: int, battery_state_of_charge_i: int,
                   battery_current_i: int, pv_dc_coupled_i: int, speed_i: int):
        self.registers["battery_power"] += battery_power_i
        self.registers["battery_state_of_charge"] -= battery_state_of_charge_i
        self.registers["battery_current"] += battery_current_i
        self.registers["pv_dc_coupled"] += pv_dc_coupled_i
        self.registers["speed"] += speed_i
        self.registers["battery_voltage"] += 1
        self.registers["pv_dc_coupled_current"] += 1

        self.registers["Course"] = randint(0, 100)
        self.registers["Latitude"] = randint(0, 100)
        self.registers["Latitude2"] = randint(0, 100)
        self.registers["Longitude"] = randint(0, 100)
        self.registers["Longitude2"] = randint(0, 100)
        self.registers["GPS fix"] = randint(0, 1)
        self.registers["GPS number of satellites"] = randint(0, 5)
        self.registers["Altitude"] = randint(0, 120)


server = ModbusServer("127.0.0.1", 502, no_block=True, data_bank=piDataBank())

try:
    print("Starting Server...")
    server.start()
    print("Server is Online")
    while True:
        continue
except:
    print("Shutdown server...")
    server.stop()
    print("Server is offline")
