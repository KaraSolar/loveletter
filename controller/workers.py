import threading


class WorkerModbus(threading.Thread):
    def __init__(self):
        super().__init__()



worker_modbus = WorkerModbus()
worker_modbus.start()