'''
TO DOS:
    For the new frames, make them destroy instead of being there.

We adhere to the recommendation of keeping a database connection in only one thread
and not passing it to other threads will remain open in second worker. There is a way to parse a conn
to another thread by setting the check_same_thread = False in sqlite3, however, that will complicate
more the software will little to no gain. This also applies for modbus tcp connection,
it will remain open in first worker and not be passed anywhere else (this module pymodbus is not
thread safe).

Note Daemon threads are abruptly stopped at shutdown. Their resources (such as open files,
database transactions, etc.) may not be released properly. If you want your threads to stop gracefully,
make them non-daemonic and use a suitable signalling mechanism such as an Event.
'''

import threading
import queue
from .view_controller import ViewController
from workers import WorkerDatabase, WorkerModbus

class Controller:
    def __init__(self, view):
        self.view = view
        self.stop_workers_signal = threading.Event()
        self.trip_mode_flag_signal = threading.Event()
        self.queue_worker_database = queue.Queue(maxsize=0)
        self.queue_main_thread = queue.Queue(maxsize=0)
        self.lock = threading.Lock()

        self.view_controller = ViewController(self.view, self.data_base_queue, self.registers_lock,
                                              self.data_bus, self.trip_start_signal_event)
        self.closing_keys()
        self.first_worker = threading.Thread(target=self.modbus_query_worker)
        self.first_worker.start()
        self.second_worker = threading.Thread(target=self.telemetry_database_worker)
        self.second_worker.start()
        self.loop_update_view()


    def closing_keys(self):
        self.view.root.bind('<Escape>', self.close_on_escape)

    def close_on_escape(self,event=None):
        print("cerrando el programa...")
        self.trip_start_signal_event.set()  # break wait time for next query
        self.modbus_query_worker_destroy_event.set() # destroy modbus
        with self.registers_lock:
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
            if status_first_worker is False and status_second_worker is False:
                break
        return 0

    def loop_update_view(self):
        self.view_controller.update_view()
        self.view.root.after(1000, self.loop_update_view)

