from pymodbus.exceptions import ModbusException, ModbusIOException, ConnectionException
from pymodbus.client.sync import ModbusTcpClient
import logging
import re


logging.basicConfig(level=logging.DEBUG, filename=f"loggings/modbus_query.log",
                    filemode="a", format="%(asctime)s - %(levelname)s - %(message)s")


class ModbusQuery:
    def __init__(self, server_ip: str = "127.0.0.1"):  # Default of the simulation of course this changes
        """Initialize a ModbusQuery object.
        Args:
            server_ip (str, optional): The IP address of the Modbus server.
                Defaults to "127.0.0.1" for simulation purposes.
        Notes:
            The client is automatically connected to the server upon initialization.
            Even if the connection fails, the socket will be opened when querying registers.
        """
        self.server_ip = server_ip
        self.server_port = 502
        self.client = ModbusTcpClient(self.server_ip, port=self.server_port)
        self.client.connect()  # even if false when querying the registers the socket will be opened.
        self.__register_values = None

    @property  # Getter
    def server_ip(self) -> str:
        """Get the server IP address."""
        return self._server_ip

    @server_ip.setter  # Setter
    def server_ip(self, server_ip: str) -> None:
        """Set the server IP address.
        Args:
            server_ip (str): The IP address to set.
        Raises:
            ValueError: If the provided IP address is not a valid IPv4 address.
        """
        ipv4_regex = r'^(\d{1,3}\.){3}\d{1,3}$'
        if re.match(ipv4_regex, server_ip) is None:
            raise ValueError("Not a valid IP address.")
        self._server_ip = server_ip

    def read_registers(self, address: int, count: int, unit: int = 100) -> list:
        """
        This function encapsulates the reading of holding registers. The function has been type
        hinted: param 1 is expected to be an int, param 2 int, param 2 int. The function returns a list.
        :param address: address of the holding register to read, see Victron documentation for address reference.
        :param count: the number of registers to read
        :param unit: defaults 100. The unit id from where to read, see Victron documentation
        :return: list containing the value of that register (sensor).
        """
        try:
            response = self.client.read_holding_registers(address=address, count=count, unit=unit)
            response = response.registers
        except (ModbusIOException, ModbusException, ConnectionException, AttributeError) as exe:
            logging.exception("during reading register")
            raise exe
        else:
            return response

    def read_telemetry_registers(self) -> None:
        """
        This function encapsulates the reading of relevant telemetry registers. Addresses: 840-843,
        850-851, 2800-2809. If an error is encountered due to connection or another when reading
        any of these holding registers (any of them) will re raise the exception. If the method
        doesn't encounter any error it will write the data into a tuple register_values.
        Tuples maintain order and allow duplicates.
        :return: None
        """
        try:
            battery_regs = self.read_registers(address=840, count=4)  # 840 to 843
            solar_regs = self.read_registers(address=850, count=2)  # 850 to 851
            georef_regs = self.read_registers(address=2800, count=10)  # 2800 to 2809
        except (ModbusIOException, ModbusException, ConnectionException, AttributeError) as exe:
            logging.exception("during reading of telemetry")
            raise exe
        else:
            self.__register_values = battery_regs + solar_regs + georef_regs

    def set_register_values_to_none(self) -> None:
        """
        This function encapsulates replacing every value in the registers value list to None.
        :return: None
        """
        number_of_registers = 16
        self.__register_values = [None] * number_of_registers

    def set_scaling(self) -> None:
        """
        This function encapsulates the need to scale some sensor readings, as per victron documentation.
        The following registers (to display in the GUI) are scaled:
        battery_voltage -> register_values 0
        battery_current -> register_values 1
        pv-dc-coupled_current -> register_values 5
        speed -> register 11
        :return: None
        """
        for index in (0, 1, 5):
            self.__register_values[index] = self.__register_values[index] / 10
        self.__register_values[11] = self.__register_values[11] / 100

    def set_negative_values(self) -> None:
        """
        Some registers can have negative values (INT16 -32,768 to 32,767) but modbus only transfers
        blocks of UINT 16 0 to 65,535 (2^16 - 1).
        The following registers (to display in the GUI) are verified for negatives:
        battery_current -> register_values 1
        battery_power -> register_values 2
        pv-dc-coupled_current -> register_values 5
        :return: None
        """
        for index in (1, 2, 5):
            if self.__register_values[index] >= 32768:
                self.__register_values[index] = self.__register_values[index] - 65536

    def read_and_format_telemetry_registers(self) -> list:
        """
        This method uses read_telemetry_registers, set_scaling, set_negative_values and
        set_register_values_to_none.
        Encapsulates every procedure for querying the modbus, set the scaling and set negative values
        and stores the telemetry values in the telemetry list and returns a copy of that list.
        :return: list
        """
        try:
            self.read_telemetry_registers()
        except (ModbusIOException, ModbusException, ConnectionException, AttributeError):
            self.set_register_values_to_none()
        else:
            self.set_scaling()
            self.set_negative_values()
        return self.__register_values.copy()

    def disconnect(self) -> int:
        """
        Disconnects the modbus tcp client closing the socket. The underlying library verifies if
        connection is open.
        :return: int when succeed
        """
        self.client.close()
        return 0
