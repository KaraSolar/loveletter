class ViewController():
    def __init__(self, view, data_base_queue, registers_lock, data_bus, modbus_loop_break):
        self.view = view
        self.data_base_queue = data_base_queue
        self.registers_lock = registers_lock
        self.data_bus = data_bus
        self.modbus_loop_break = modbus_loop_break
        self.configure_data_display_buttons()
        self.configure_passenger_input_buttons()
        self.configure_initiate_trip_frame_buttons()
        self.configure_finish_trip_frame_buttons()

    def configure_data_display_buttons(self):
        self.view.data_display_frame.center_pane.end_trip_button.config(command=lambda:self.view.raise_frame("finish_trip_frame"))
        self.view.data_display_frame.center_pane.start_trip_button.config(command=lambda:self.view.raise_frame("passenger_input_frame"))

    def configure_passenger_input_buttons(self):
        self.view.passenger_input_frame.start_trip_button.config(command=self.change_initiate_trip_frame)
        self.view.passenger_input_frame.go_back_button.config(command=lambda: self.view.raise_frame("data_display_frame"))

    def change_initiate_trip_frame(self):
        self.view.initiate_trip_frame.set_initiate_trip_text_var()
        self.view.raise_frame("initiate_trip_frame")

    def configure_initiate_trip_frame_buttons(self):
        self.view.initiate_trip_frame.no_button.config(command=lambda: self.view.raise_frame("passenger_input_frame"))
        self.view.initiate_trip_frame.yes_button.config(command=self.initiate_trip_listener)

    def initiate_trip_listener(self):
        passenger_number = self.view.passenger_input_frame.passenger_number_var.get()
        self.view.data_display_frame.show_trip_mode()
        self.view.raise_frame("data_display_frame")
        self.data_base_queue.put(passenger_number)
        with self.registers_lock:
            self.data_bus["sampling_rate"] = 1
            self.modbus_loop_break.set()

    def configure_finish_trip_frame_buttons(self):
        self.view.finish_trip_frame.no_button.config(command=lambda: self.view.raise_frame("data_display_frame"))
        self.view.finish_trip_frame.yes_button.config(command=self.end_trip_listener)

    def end_trip_listener(self):
        self.view.data_display_frame.show_dock_mode()
        self.data_base_queue.put("end_of_trip")
        with self.registers_lock:
            self.data_bus["sampling_rate"] = 15
        self.view.raise_frame("data_display_frame")
        self.modbus_loop_break.clear()

    def update_view(self) -> None:
        with self.registers_lock:
            # Battery Power
            self.view.data_display_frame.left_pane.battery_power_variable.set(self.data_bus["telemetry"]["battery_power"])
            # Battery State of Charge
            if self.data_bus["telemetry"]["battery_state_of_charge"] is not None:
                self.view.data_display_frame.left_pane.battery_soc_percentage_flood_gauge.configure(value=self.data_bus["telemetry"]["battery_state_of_charge"])
            else:
                self.view.data_display_frame.left_pane.battery_soc_percentage_flood_gauge.configure(value=-1)
            # Solar Power
            self.view.data_display_frame.right_pane.solar_power_variable.set(self.data_bus["telemetry"]["pv-dc-coupled_power"])
            # Load Power
            try:
                load = self.data_bus["telemetry"]["battery_power"]-self.data_bus["telemetry"]["pv-dc-coupled_power"]
            except TypeError:
                load = None
            self.view.data_display_frame.right_pane.load_power_variable.set(load)
            # Speed
            if self.data_bus["telemetry"]["speed"] is not None:
                self.view.data_display_frame.center_pane.speed_indicator.configure(amountused = self.data_bus["telemetry"]["speed"])
            else:
                self.view.data_display_frame.center_pane.speed_indicator.configure(amountused = 0)
        return 0