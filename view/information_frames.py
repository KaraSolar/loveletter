import ttkbootstrap as ttk
import signal
import os

class InitiateTripFrame(ttk.Frame):
    def __init__(self, master: ttk.Window, passenger_number_var: ttk.IntVar, trip_purposes_var: ttk.StringVar,
                 captains_var: ttk.StringVar, multi_leg_trip_var: ttk.BooleanVar,
                 dep_community_var: ttk.StringVar, dep_port_var: ttk.StringVar,
                 arr_community_var: ttk.StringVar, arr_port_var: ttk.StringVar):
        super().__init__(master)
        self.passenger_number_var = passenger_number_var
        self.trip_purposes_var = trip_purposes_var
        self.captains_var = captains_var
        self.multi_leg_trip_var = multi_leg_trip_var
        self.dep_community_var = dep_community_var
        self.dep_port_var = dep_port_var
        self.arr_community_var = arr_community_var
        self.arr_port_var = arr_port_var

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)   # Title row
        self.rowconfigure(1, weight=6)   # Labels row
        self.rowconfigure(2, weight=1)   # Navigation row

        self.initiate_trip_text_var_pass_number = ttk.StringVar()
        self.initiate_trip_text_var_trip_purpose = ttk.StringVar()
        self.initiate_trip_text_var_captain = ttk.StringVar()
        self.initiate_trip_text_var_multiple_dest = ttk.StringVar()
        self.initiate_trip_text_var_departure = ttk.StringVar()
        self.initiate_trip_text_var_arrival = ttk.StringVar()

        self._build_title_frame()
        self._build_labels_frame()
        self._build_navigation_frame()

    def _build_title_frame(self) -> None:
        title_frame = ttk.Frame(self, padding=(10, 8))
        title_frame.grid(row=0, column=0, sticky="nsew")
        title_frame.columnconfigure(0, weight=1)
        ttk.Label(
            title_frame,
            text="Iniciar viaje con:",
            font=("Digital-7", 21),
            anchor="center",
        ).grid(row=0, column=0, sticky="ew")

    def _build_labels_frame(self) -> None:
        labels_frame = ttk.Frame(self)
        labels_frame.grid(row=1, column=0, sticky="nsew")
        labels_frame.columnconfigure(0, weight=1)
        for r in range(6):
            labels_frame.rowconfigure(r, weight=1)

        label_vars = [
            self.initiate_trip_text_var_pass_number,
            self.initiate_trip_text_var_captain,
            self.initiate_trip_text_var_trip_purpose,
            self.initiate_trip_text_var_multiple_dest,
            self.initiate_trip_text_var_departure,
            self.initiate_trip_text_var_arrival,
        ]
        for i, var in enumerate(label_vars):
            ttk.Label(
                labels_frame,
                textvariable=var,
                font=("Digital-7", 21),
                anchor="center",
            ).grid(row=i, column=0, sticky="ew")

    def _build_navigation_frame(self) -> None:
        nav_frame = ttk.Frame(self, padding=(12, 8))
        nav_frame.grid(row=2, column=0, sticky="nsew")
        nav_frame.columnconfigure(0, weight=1)
        nav_frame.columnconfigure(1, weight=0)
        nav_frame.columnconfigure(2, weight=1)
        nav_frame.rowconfigure(0, weight=1)

        self.no_button = ttk.Button(
            master=nav_frame,
            text="← Regresar",
            style="info.Outline.TButton",
            width=16,
        )
        self.no_button.grid(row=0, column=0, sticky="e", padx=(0, 10))

        ttk.Label(nav_frame, text="", width=4).grid(row=0, column=1)

        self.yes_button = ttk.Button(
            master=nav_frame,
            text="Continuar →",
            style="info.TButton",
            width=16,
        )
        self.yes_button.grid(row=0, column=2, sticky="w", padx=(10, 0))

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

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)   # Title row
        self.rowconfigure(1, weight=6)   # Content row
        self.rowconfigure(2, weight=1)   # Navigation row

        self._build_title_frame()
        self._build_content_frame()
        self._build_navigation_frame()

    def _build_title_frame(self) -> None:
        title_frame = ttk.Frame(self, padding=(10, 8))
        title_frame.grid(row=0, column=0, sticky="nsew")
        title_frame.columnconfigure(0, weight=1)
        ttk.Label(
            title_frame,
            text="Terminar Viaje",
            font=("Digital-7", 22),
            anchor="center",
        ).grid(row=0, column=0, sticky="ew")

    def _build_content_frame(self) -> None:
        content_frame = ttk.Frame(self)
        content_frame.grid(row=1, column=0, sticky="nsew")
        content_frame.columnconfigure(0, weight=1)
        content_frame.rowconfigure(0, weight=1)
        ttk.Label(
            content_frame,
            text="Está seguro que quiere terminar el viaje?",
            font=("Digital-7", 22),
            anchor="center",
            wraplength=400,
        ).grid(row=0, column=0, sticky="ew")

    def _build_navigation_frame(self) -> None:
        nav_frame = ttk.Frame(self, padding=(12, 8))
        nav_frame.grid(row=2, column=0, sticky="nsew")
        nav_frame.columnconfigure(0, weight=1)
        nav_frame.columnconfigure(1, weight=0)
        nav_frame.columnconfigure(2, weight=1)
        nav_frame.rowconfigure(0, weight=1)

        self.no_button = ttk.Button(
            master=nav_frame,
            text="← Regresar",
            style="info.Outline.TButton",
            width=16,
        )
        self.no_button.grid(row=0, column=0, sticky="e", padx=(0, 10))

        ttk.Label(nav_frame, text="", width=4).grid(row=0, column=1)

        self.yes_button = ttk.Button(
            master=nav_frame,
            text="Si →",
            style="info.TButton",
            width=16,
        )
        self.yes_button.grid(row=0, column=2, sticky="w", padx=(10, 0))


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
        elif frame == "biodiversity_input_frame":
            self.warning_text_var.set("Selecciona una especie primero.")
        else:
            print("Algo salio mal, abortando...")
            os.kill(os.getpid(), signal.SIGINT)
