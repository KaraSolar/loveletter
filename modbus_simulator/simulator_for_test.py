from pyModbusTCP.server import ModbusServer, DataBank


class piDataBank(DataBank):
    def __init__(self):
        super().__init__(h_regs_size=3000) # max register used for the sim is 2808 so 3000 rounded.
        self.registers = {
            "battery_voltage": 0,
            "battery_power": 0,
            "battery_state_of_charge": 0,
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
            "Altitude": 0,
            "Altitude2": 0}

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
        self._h_regs[2809] = self.registers["Altitude2"]

        self.increasers()
        try:
            return [round(self._h_regs[i]) for i in range(address, address + number)]
        except KeyError:
            return

    def increasers(self):
        for key in self.registers:
            self.registers[key] += 1


server = ModbusServer("127.0.0.1", 502, no_block=True, data_bank=piDataBank())

def run_server():
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

if __name__ == "__main__":
    run_server()