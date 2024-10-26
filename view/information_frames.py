import ttkbootstrap as ttk


class InitiateTripFrame(ttk.Frame):
    def __init__(self, master: ttk.Window, passenger_number_var: ttk.IntVar, trip_purposes_var: ttk.StringVar):
        super().__init__(master)
        self.passenger_number_var = passenger_number_var
        self.trip_purposes_var = trip_purposes_var
        self.columnconfigure((0, 1), weight=1, uniform="a")
        self.rowconfigure((0, 1), weight=1, uniform="a")
        self.initiate_trip_text_var_pass_number = ttk.StringVar()
        self.initiate_trip_text_var_trip_purpose = ttk.StringVar()
        self.labels_frame = ttk.Frame(self)
        self.labels_frame.columnconfigure(0, weight=1, uniform="a")
        self.labels_frame.rowconfigure((0, 1), weight=1, uniform="a")
        self.labels_frame.grid(row=0, column=0, columnspan=2, sticky="nsew")
        self.initiate_trip_label = ttk.Label(master=self.labels_frame,
                                             textvariable=self.initiate_trip_text_var_pass_number,
                                             font=("Digital-7", 21))
        self.initiate_trip_label.grid(row=0, column=0, sticky="s")
        self.initiate_trip_label = ttk.Label(master=self.labels_frame,
                                             textvariable=self.initiate_trip_text_var_trip_purpose,
                                             font=("Digital-7", 21))
        self.initiate_trip_label.grid(row=1, column=0)
        self.yes_no_buttons()

    def yes_no_buttons(self):
        self.yes_button = ttk.Button(master=self,
                                     text="Si",
                                     style="info.TButton")

        self.no_button = ttk.Button(master=self,
                                    text="No",
                                    style="info.TButton")

        self.yes_button.grid(row=1, column=1, sticky="nw", padx=50)

        self.no_button.grid(row=1, column=0, sticky="ne", padx=50)

    def set_initiate_trip_text_var(self):
        string_pass = f"Está seguro que quiere iniciar el viaje con {self.passenger_number_var.get()} pasajeros?"
        self.initiate_trip_text_var_pass_number.set(string_pass)
        string_trip_purpose = f"Y motivo de viaje: {self.trip_purposes_var.get()}?"
        self.initiate_trip_text_var_trip_purpose.set(string_trip_purpose)


class FinishTripFrame(ttk.Frame):
    def __init__(self, master: ttk.Window):
        super().__init__(master)
        self.columnconfigure((0, 1), weight=1, uniform="a")
        self.rowconfigure((0, 1), weight=1, uniform="a")
        self.end_trip_label = ttk.Label(master=self,
                                        textvariable="Está seguro que quiere terminar el viaje?",
                                        font=("Digital-7", 22))
        self.end_trip_label.grid(row=0, column=0, columnspan=2)
        self.yes_no_buttons()

    def yes_no_buttons(self):
        self.yes_button = ttk.Button(master=self,
                                     text="Si",
                                     style="info.TButton")

        self.no_button = ttk.Button(master=self,
                                    text="No",
                                    style="info.TButton")

        self.yes_button.grid(row=1, column=1, sticky="nw", padx=50)

        self.no_button.grid(row=1, column=0, sticky="ne", padx=50)


class TripPurposeWarning(ttk.Frame):
    def __init__(self, master: ttk.Window, trip_purposes_var: ttk.StringVar):
        super().__init__(master)
        self.trip_purposes_var = trip_purposes_var
        self.warning_text_var = ttk.StringVar()
        self.columnconfigure((0, 1), weight=1, uniform="a")
        self.rowconfigure((0, 1), weight=1, uniform="a")
        self.trip_purpose_warning_label = ttk.Label(master=self,
                                                    textvariable=self.warning_text_var,
                                                    font=("Digital-7", 21))
        self.trip_purpose_warning_label.grid(row=0, column=0, columnspan=2)
        self.close_warning_button = ttk.Button(master=self,
                                               text="Cerrar",
                                               style="info.TButton")
        self.close_warning_button.grid(row=1, column=0, columnspan=2)

    def set_warning_text_var(self):
        self.warning_text_var.set(f"El motivo de viaje: {self.trip_purposes_var.get()} no es válido.")