"""
TO DOS:
    For the new frames, make them destroy instead of being there.

"""

import time
import threading
import queue
from .view_controller import ViewController
from .workers import WorkerDatabase, WorkerModbus


class Controller:
    def __init__(self, view, db_name):
        self.view = view
        self.db_name = db_name
        self.view.root.bind("<<update_view>>", self.update_view)
        self.stop_workers_signal = threading.Event()
        self.trip_mode_flag_signal = threading.Event()
        self.queue_worker_database = queue.Queue(maxsize=0)
        self.queue_view = queue.Queue(maxsize=0)
        self.view_controller = ViewController(self.view, self.queue_worker_database,  self.trip_mode_flag_signal)
        self.closing_keys()
        self.worker_modbus = WorkerModbus(queue_worker_database=self.queue_worker_database,
                                          stop_workers_signal=self.stop_workers_signal,
                                          event_generate=self.view.root.event_generate,
                                          trip_mode_flag_signal=self.trip_mode_flag_signal,
                                          queue_view=self.queue_view)
        self.worker_modbus.start()
        self.worker_database = WorkerDatabase(queue_worker_database=self.queue_worker_database,
                                              db_name=self.db_name)
        self.worker_database.start()

    def closing_keys(self):
        self.view.root.bind('<Escape>', self.close_on_escape)

    def close_on_escape(self, event=None):
        print("cerrando el programa...")
        self.trip_mode_flag_signal.set()  # break wait time for next query
        self.stop_workers_signal.set()  # destroy modbus
        self.queue_worker_database.put({"type": "destroy"})
        # Join blocks the main thread freezing the GUI
        self.worker_modbus.join()
        self.worker_database.join()
        self.closing()
        self.view.root.destroy()

    def closing(self):
        """
        Verifies if the threads are alive to close the entire program.
        The user can't make any changes in the program.
        TO DO:
        Might be useful to extend this to prompt the user for closing verification.
        """
        while self.worker_modbus.is_alive() or self.worker_database.is_alive():
            time.sleep(0.1)
        return 0

    def update_view(self, event):
        telemetry = self.queue_view.get()
        self.view_controller.update_view(telemetry)
