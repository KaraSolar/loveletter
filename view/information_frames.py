import ttkbootstrap as ttk
import signal
import os

class InitiateTripFrame(ttk.Frame):
    def __init__(self, master: ttk.Window, passenger_number_var: ttk.IntVar, trip_purposes_var: ttk.StringVar,
                 captains_var: ttk.StringVar, multi_leg_trip_var: ttk.BooleanVar,
                 dep_community_var: ttk.StringVar, dep_port_var: ttk.StringVar,
                 arr_community_var: ttk.StringVar, arr_port_var: ttk.StringVar):
        super().__init__(master)
        # Class args
        self.passenger_number_var = passenger_number_var
        self.trip_purposes_var = trip_purposes_var
        self.captains_var = captains_var
        self.multi_leg_trip_var = multi_leg_trip_var
        self.dep_community_var = dep_community_var
        self.dep_port_var = dep_port_var
        self.arr_community_var = arr_community_var
        self.arr_port_var = arr_port_var

        # class frame configuration
        self.columnconfigure((0, 1), weight=1, uniform="a")
        self.rowconfigure((0, 1), weight=1, uniform="a")
        self.labels_frame = ttk.Frame(self)
        self.labels_frame.columnconfigure(0, weight=1, uniform="a")
        self.labels_frame.rowconfigure((0, 1, 2, 3, 4, 5, 6), weight=1, uniform="a")

        # displaying vars
        self.initiate_trip_text_var_pass_number = ttk.StringVar()
        self.initiate_trip_text_var_trip_purpose = ttk.StringVar()
        self.initiate_trip_text_var_captain = ttk.StringVar()
        self.initiate_trip_text_var_multiple_dest = ttk.StringVar()
        self.initiate_trip_text_var_departure = ttk.StringVar()
        self.initiate_trip_text_var_arrival = ttk.StringVar()


        # Frame packing
        self.labels_frame.grid(row=0, column=0, columnspan=2, sticky="nsew")
        self.initiate_trip_title = ttk.Label(master=self.labels_frame,
                                             text="Iniciar viaje con:",
                                             font=("Digital-7", 21))
        self.initiate_trip_title.grid(row=0, column=0, sticky="n")
        self.initiate_trip_label_passenger_number = ttk.Label(master=self.labels_frame,
                                                              textvariable=self.initiate_trip_text_var_pass_number,
                                                              font=("Digital-7", 21))
        self.initiate_trip_label_passenger_number.grid(row=1, column=0)
        self.initiate_trip_label_captain = ttk.Label(master=self.labels_frame,
                                                     textvariable=self.initiate_trip_text_var_captain,
                                                     font=("Digital-7", 21))
        self.initiate_trip_label_captain.grid(row=2, column=0)
        self.initiate_trip_label_trip_purpose = ttk.Label(master=self.labels_frame,
                                                          textvariable=self.initiate_trip_text_var_trip_purpose,
                                                          font=("Digital-7", 21))
        self.initiate_trip_label_trip_purpose.grid(row=3, column=0)
        self.initiate_trip_label_multiple_dest = ttk.Label(master=self.labels_frame,
                                                           textvariable=self.initiate_trip_text_var_multiple_dest,
                                                           font=("Digital-7", 21))
        self.initiate_trip_label_multiple_dest.grid(row=4, column=0)
        self.initiate_trip_label_departure = ttk.Label(master=self.labels_frame,
                                                           textvariable=self.initiate_trip_text_var_departure,
                                                           font=("Digital-7", 21))
        self.initiate_trip_label_departure.grid(row=5, column=0)
        self.initiate_trip_label_arrival = ttk.Label(master=self.labels_frame,
                                                           textvariable=self.initiate_trip_text_var_arrival,
                                                           font=("Digital-7", 21))
        self.initiate_trip_label_arrival.grid(row=6, column=0)

        self.yes_no_buttons()

    def yes_no_buttons(self):
        self.yes_button = ttk.Button(master=self,
                                     text="Continuar →",
                                     style="info.TButton")

        self.no_button = ttk.Button(master=self,
                                    text="← Regresar",
                                    style="info.TButton")

        self.yes_button.grid(row=1, column=1, sticky="nw", padx=50, pady=100)

        self.no_button.grid(row=1, column=0, sticky="ne", padx=50, pady=100)

    def set_initiate_trip_text_var(self):
        string_pass = f"Pasajeros: {self.passenger_number_var.get()}"
        self.initiate_trip_text_var_pass_number.set(string_pass)
        string_captain = f"Capitán: {self.captains_var.get()}"
        self.initiate_trip_text_var_captain.set(string_captain)
        string_trip_purpose = f"Motivo: {self.trip_purposes_var.get()}"
        self.initiate_trip_text_var_trip_purpose.set(string_trip_purpose)
        string_multiple_dest = f"Destino Multiple: {'Si' if self.multi_leg_trip_var.get() == True else 'No'}"
        self.initiate_trip_text_var_multiple_dest.set(string_multiple_dest)
        string_departure_info = f"Salida: {self.dep_community_var.get()}-{self.dep_port_var.get()}"
        self.initiate_trip_text_var_departure.set(string_departure_info)
        string_arrival_info = f"Llegada: {self.arr_community_var.get()}-{self.arr_port_var.get()}"
        self.initiate_trip_text_var_arrival.set(string_arrival_info)

class FinishTripFrame(ttk.Frame):
    def __init__(self, master: ttk.Window):
        super().__init__(master)
        self.columnconfigure((0, 1), weight=1, uniform="a")
        self.rowconfigure((0, 1), weight=1, uniform="a")
        self.end_trip_label = ttk.Label(master=self,
                                        text="Está seguro que quiere terminar el viaje?",
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
        self.rowconfigure((0, 1, 2), weight=1, uniform="a")
        self.trip_purpose_warning_label = ttk.Label(master=self,
                                                    textvariable=self.warning_text_var,
                                                    font=("Digital-7", 21))
        self.trip_purpose_warning_label.grid(row=0, column=0, columnspan=2)
        self.trip_purpose_warning_label_two = ttk.Label(master=self,
                                                    text="Por favor, seleccione uno.",
                                                    font=("Digital-7", 21))
        self.trip_purpose_warning_label_two.grid(row=1, column=0, columnspan=2)
        self.close_warning_button = ttk.Button(master=self,
                                               text="Cerrar",
                                               style="info.TButton")
        self.close_warning_button.grid(row=2, column=0, columnspan=2)

    def set_warning_text_var(self, frame):
        if frame == "multi_leg_trip_frame":
            self.warning_text_var.set("Motivo de viaje no válido")
        elif frame == "trip_purposes_frame":
            self.warning_text_var.set("Capitán no válido.")
        elif frame == "departure_port_frame":
            self.warning_text_var.set("Selecciona una comunidad de salida.")
        elif frame == "arrival_community_frame":
            self.warning_text_var.set("Selecciona un puerto o finca de salida.")
        elif frame == "arrival_port_frame":
            self.warning_text_var.set("Selecciona una comunidad de llegada.")
        elif frame == "initiate_trip_frame":
            self.warning_text_var.set("Selecciona un puerto o finca de llegada.")
        else:
            print("Algo salio mal, abortando...")
            os.kill(os.getpid(), signal.SIGINT)
