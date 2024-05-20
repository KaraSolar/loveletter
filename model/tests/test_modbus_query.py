"""
Note:
Keep in mind that the simulator_for_test starts at 0 and for each querying it increases the value by 1.
for every register in 840 to 843, 850 to 851, 2800 to 2809. Note that the scope of the fixture methods
is set to function, keeping each test independent of each other.
"""

import pytest
from pymodbus.client.sync import ModbusTcpClient
from pymodbus.exceptions import ConnectionException
from model.modbus_query import ModbusQuery
from modbus_simulator.simulator_for_test import run_server
import multiprocessing
import time


@pytest.fixture(scope="function", autouse=True)
def start_server() -> multiprocessing.Process:
    start_server = multiprocessing.Process(target=run_server)
    start_server.start()
    time.sleep(2)
    yield start_server
    start_server.terminate()  # clean up after tests are done


@pytest.fixture(scope="function", autouse=True)
def modbus_object(start_server):
    modbus_object = ModbusQuery()
    yield modbus_object
    modbus_object.disconnect()


def test_getters_setters():
    with pytest.raises(ValueError):
        ModbusQuery(server_ip="cat")
    with pytest.raises(ValueError):
        ModbusQuery(server_ip=" 127.0.0.1")


def test_init_method():
    """
    make sure that the server_ip works with a correct ip, port is 502.
    """
    modbus_query_init = ModbusQuery("139.112.255.0")
    assert modbus_query_init.server_ip == "139.112.255.0"
    assert modbus_query_init.server_port == 502
    assert type(modbus_query_init.client) == ModbusTcpClient
    modbus_query_init.disconnect()


def test_read_registers(modbus_object):
    """
    The last test that access an address that is not included in the simulator (40000) will disconnect
    from the simulated server. Throwing an exception
    """
    modbus_query = modbus_object
    response = modbus_query.read_registers(840, 1)
    assert response == [0]  # Counter is at 0
    response = modbus_query.read_registers(840, 1)
    assert response == [1]  # Counter is at 1
    with pytest.raises(ConnectionException):
        modbus_query.read_registers(40000, 1)


def test_set_register_values_to_none(modbus_object):
    expected_values = [None] * 16
    modbus_object._ModbusQuery__register_values = [8] * 16
    modbus_object.set_register_values_to_none()
    assert modbus_object._ModbusQuery__register_values == expected_values
    modbus_object._ModbusQuery__register_values = ["cat"] * 16
    modbus_object.set_register_values_to_none()
    assert modbus_object._ModbusQuery__register_values == expected_values


def test_set_telemetry_from_register_values(modbus_object):
    modbus_object._ModbusQuery__register_values = [100, 200, 500, 20, 20, 1000, 0, 0, 0, 0, 0, 10000,
                                                   12, 12, 12, 12]
    modbus_object.set_telemetry_from_register_values()
    expected_values = {"battery_voltage": 100, "battery_current": 200,
                              "battery_power": 500, "battery_state_of_charge": 20,
                              "pv-dc-coupled_power": 20, "pv-dc-coupled_current": 1000,
                              "latitude1": 0, "latitude2": 0, "longitude1": 0,
                              "longitude2": 0, "course": 0, "speed": 10000,
                              "gps_fix": 12, "gps_number_of_satellites": 12,
                              "altitude1": 12, "altitude2": 12}
    assert modbus_object._ModbusQuery__telemetry == expected_values
    modbus_object._ModbusQuery__register_values = [None] * 16
    modbus_object.set_telemetry_from_register_values()
    assert modbus_object._ModbusQuery__telemetry["battery_voltage"] == None


def test_set_scaling(modbus_object):
    modbus_object._ModbusQuery__register_values = [100, 200, 500, 20, 20, 1000, 0, 0, 0, 0, 0, 10000,
                                                   12, 12, 12, 12]
    modbus_object.set_telemetry_from_register_values()
    modbus_object.set_scaling()
    assert modbus_object._ModbusQuery__telemetry["battery_voltage"] == 10
    assert modbus_object._ModbusQuery__telemetry["battery_current"] == 20
    assert modbus_object._ModbusQuery__telemetry["pv-dc-coupled_current"] == 100
    assert modbus_object._ModbusQuery__telemetry["speed"] == 100
    modbus_object._ModbusQuery__telemetry = {key: "cat" for key in modbus_object._ModbusQuery__telemetry}
    with pytest.raises(TypeError):
        modbus_object.set_scaling()


def test_set_negative_values(modbus_object):
    # Handy reference for conversion: https://www.simonv.fr/TypesConvert/?integers
    modbus_object._ModbusQuery__register_values = [100, 63000, 32767, 20, 20, 65536, 0, 0, 0, 0, 0, 10000,
                                                   12, 12, 12, 12]
    modbus_object.set_telemetry_from_register_values()
    modbus_object.set_negative_values()
    assert modbus_object._ModbusQuery__telemetry["battery_current"] == -2536
    assert modbus_object._ModbusQuery__telemetry["battery_power"] == 32767
    assert modbus_object._ModbusQuery__telemetry["pv-dc-coupled_current"] == 0
    modbus_object._ModbusQuery__telemetry = {key: "cat" for key in modbus_object._ModbusQuery__telemetry}
    with pytest.raises(TypeError):
        modbus_object.set_negative_values()


def test_read_telemetry_registers(modbus_object):
    try:
        modbus_object.read_registers(40000, 1)  # Loose connection to server
    except ConnectionException:
        pass
    modbus_object.read_telemetry_registers()
    battery_regs = modbus_object._ModbusQuery__register_values[0:4]
    solar_regs = modbus_object._ModbusQuery__register_values[4:6]
    georef_regs = modbus_object._ModbusQuery__register_values[6::]
    assert len(modbus_object._ModbusQuery__register_values) == 16
    assert battery_regs == [1] * 4  # Counter is at 1
    assert solar_regs == [2] * 2  # Counter is at 2
    assert georef_regs == [3] * 10  # Counter is at 3


def test_read_and_format_telemetry_registers(modbus_object):
    # Integration test
    modbus_object.read_registers(840, 1)
    modbus_object.read_and_format_telemetry_registers()  # Increase 3 values
    modbus_object.read_and_format_telemetry_registers()  # Increase 3 more values

    telemetry = modbus_object.read_and_format_telemetry_registers()
    assert type(telemetry) == dict
    assert id(telemetry) != id(modbus_object._ModbusQuery__telemetry)
    assert telemetry["battery_voltage"] == 0.7
    assert telemetry["latitude1"] == 9
    assert telemetry["altitude2"] == 9


# Nesting two functions for this test. --> ask chatgpt how to organize an integration test.
def test_read_registers_and_read_telemetry_registers_disconnection(start_server, modbus_object):
    """
    Integration test.
    testing the sudden termination of the server.
    After the disconnection of the server for hours the client object still maintains the socket
    but then the .registers method will raise an AttributeError, 'ModbusIOException' object
    has no attribute 'registers'. If continuing sending requests when disconnected pymodbus raises
    ConnectionException, failed to connect [ModbusTcpClient(127.0.0.1:502)]
    """
    modbus_query = modbus_object
    p = start_server
    response = modbus_query.read_registers(840, 1)
    assert response == [0]  # Counter is at 9
    p.terminate()
    time.sleep(2)
    with pytest.raises(AttributeError):
        modbus_query.read_registers(840, 1)
    time.sleep(2)
    with pytest.raises(ConnectionException):
        modbus_query.read_telemetry_registers()
    time.sleep(2)
    telemetry = modbus_query.read_and_format_telemetry_registers()
    assert all(value is None for value in telemetry.values())


def test_disconnect(modbus_object):
    """
    Not terribly important, if socket remains open the operating system garbage collector will
    eventually release it.
    """
    val = modbus_object.disconnect()
    assert val == 0
