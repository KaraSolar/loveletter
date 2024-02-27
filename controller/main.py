'''
TO DOS:
    For the new frames, make them destroy instead of being there.

This software adheres to the recomendation of keeping a database connection in only one thread
and not passing it to other threads will remain open in second worker. There is a way to parse a conn
to another thread by setting the check_same_thread = False in sqlite3, however, that will complicate
more the software will little to no gain. This also applies for modbus tcp connection,
it will remain open in first worker and not be passed anywhere else (this module pymodbus is not
thread safe).

'''

import threading
import queue
import time
from model.modbus_query import ModbusQuery
from pymodbus.exceptions import ModbusException, ModbusIOException
from model.telemetry_database import TelemetryDatabase
from .view_controller import ViewController

class Controller():
    def __init__(self, view):
        self.view = view
        self.registers_lock = threading.Lock()
        self.modbus_loop_break = threading.Event()
        self.data_base_queue = queue.Queue(maxsize=0)
        self.data_bus = {"telemetry":{"battery_voltage":None, "battery_current":None,
                                      "battery_power":None, "battery_state_of_charge":None,
                                      "pv-dc-coupled_power":None, "pv-dc-coupled_current":None,
                                      "latitude1":None, "latitude2":None, "longitude1":None,
                                      "longitude2":None, "course":None, "speed":None,
                                      "gps_fix":None, "gps_number_of_satellites":None,
                                      "altitude1":None, "altitude2":None},
                         "sampling_rate":15,
                         "destroy":False}

        self.view_controller = ViewController(self.view,self.data_base_queue, self.registers_lock,
                                              self.data_bus, self.modbus_loop_break)
        self.closing_keys()
        self.first_worker = threading.Thread(target=self.modbus_query_worker,
                                             args=(self.registers_lock,
                                                   self.data_base_queue,
                                                   self.data_bus,
                                                   self.modbus_loop_break,))
        self.first_worker.start()
        self.second_worker = threading.Thread(target=self.telemetry_database_worker,
                                              args=(self.registers_lock,
                                                    self.data_base_queue,
                                                    self.data_bus,))
        self.second_worker.start()
        self.loop_update_view()


    def closing_keys(self):
        self.view.root.bind('<Escape>', self.close_on_escape)
        self.view.root.bind('<Control-c>', self.close_on_escape)

    def close_on_escape(self,event=None):
        print("cerrando el programa...")
        with self.registers_lock:
            self.modbus_loop_break.set()
            self.data_bus["destroy"] = True
            self.data_base_queue.put("destroy")
        self.first_worker.join()
        self.second_worker.join()
        self.closing()
        self.view.root.destroy()

    def closing(self):
        '''this wile true loop will freeze the gui, after setting a closure the user can't make any changes
        in the program. Might be useful to extend this to prompt the user for closing verification.
        Might be useful for future versions.
        '''
        while True:
            status_first_worker = self.first_worker.is_alive()
            status_second_worker = self.second_worker.is_alive()
            if status_first_worker == False and status_second_worker == False:
                break
        return 0

    def loop_update_view(self):
        self.view_controller.update_view()
        self.view.root.after(1000, self.loop_update_view)

    def telemetry_database_worker(self, registers_lock, data_base_queue, data_bus):
        telemetry_database = TelemetryDatabase()
        while True:
            message = data_base_queue.get()
            if message == "destroy":
                telemetry_database.close_connection()
                break
            elif message == "telemetry":
                with registers_lock:
                    telemetry_database.insert_telemetry(data_bus["telemetry"])
            elif message == "end_of_trip":
                telemetry_database.end_of_trip()
            else:
                telemetry_database.insert_trip(message)
        return 0

    def modbus_query_worker(self, registers_lock, data_base_queue, data_bus, modbus_loop_break):
        modbus_query = ModbusQuery()
        while True:
            with registers_lock:
                if data_bus["destroy"] == True:
                    modbus_query.disconnect()
                    break
                rate = data_bus["sampling_rate"]
            try:
                modbus_query.read_telemetry_registers()
            except (ModbusIOException, ModbusException, AttributeError) as exe:
                # add to logs
                with registers_lock:
                    for key in data_bus["telemetry"]:
                        data_bus["telemetry"][key] = None
                continue
            else:
                with registers_lock:
                    for index, key in enumerate(data_bus["telemetry"]):
                        data_bus["telemetry"][key] = modbus_query.register_values[index]
                data_base_queue.put("telemetry")
            for _ in range(rate):
                if modbus_loop_break.is_set():
                    break
                time.sleep(1)
        return 0
