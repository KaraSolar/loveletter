import ttkbootstrap as ttk


class PassengerInput(ttk.Frame):
    def __init__(self, master: ttk.Window, label_font_size: tuple, passenger_number_config):
        super().__init__(master)

        # ____________Initialize Variables __________
        self.passenger_number_config = passenger_number_config
        self.max_passenger: int = self.passenger_number_config["max"]
        self.min_passenger: int = self.passenger_number_config["min"]
        self.label_font_size: tuple = label_font_size
        self.passenger_number_var: ttk.IntVar = ttk.IntVar(value=self.min_passenger)

        # ____________FrameConfiguration_____________
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)   # Title row
        self.rowconfigure(1, weight=6)   # Buttons row
        self.rowconfigure(2, weight=1)   # Navigation row
        self.center_dynamic_frame = ttk.Frame(self)
        self.center_dynamic_frame.grid(row=1, column=0, sticky="nsew")
        self.center_dynamic_frame.columnconfigure((0, 1, 2), weight=1)
        self.center_dynamic_frame.rowconfigure(0, weight=1)   # Title row

        self._build_title_frame()
        self._build_buttons_frame()
        self._build_navigation_frame()


    # _________________Methods_____________________________

    def _build_buttons_frame(self) -> None:

        # _____________Passenger Number Buttons____________

        self.decrease_passenger_button: ttk.Button = ttk.Button(master=self.center_dynamic_frame,
                                                                text="Menos",
                                                                style="info.TButton",
                                                                padding=(10, 20),
                                                                command=self.decrease_passenger_number)
        self.decrease_passenger_button.grid(row=0, column=0, sticky="ew")

        self.increase_passenger_button: ttk.Button = ttk.Button(master=self.center_dynamic_frame,
                                                                style="info.TButton",
                                                                text="Mas",
                                                                padding=(10, 20),
                                                                width=6,
                                                                command=self.increase_passenger_number)
        self.increase_passenger_button.grid(row=0, column=2, sticky="ew")

        # _______________Passenger Indicator______________
        self.passenger_number_label: ttk.Label = ttk.Label(master=self.center_dynamic_frame,
                                                           textvariable=self.passenger_number_var,
                                                           font=("Digital-7", 50))
        self.passenger_number_label.grid(row=0, column=1)


    # ________________command methods_____________________
    def refresh(self) -> None:
        self.passenger_number_var.set(self.min_passenger)

    def decrease_passenger_number(self) -> None:
        n: int = self.passenger_number_var.get()
        if n > self.min_passenger:
            self.passenger_number_var.set(n - 1)

    def increase_passenger_number(self) -> None:
        n: int = self.passenger_number_var.get()
        if n < self.max_passenger:
            self.passenger_number_var.set(n + 1)

    # _________________ Row 0 — Title _____________________________
    def _build_title_frame(self) -> None:
        title_frame = ttk.Frame(self, padding=(10, 8))
        title_frame.grid(row=0, column=0, sticky="nsew")
        title_frame.columnconfigure(0, weight=1)

        ttk.Label(
            title_frame,
            text="Seleccionar Numero de Pasajeros",
            font=(*self.label_font_size, "bold"),
            anchor="center",
        ).grid(row=0, column=0, sticky="ew")

    # _________________ Row 2 — Navigation _______________________
    def _build_navigation_frame(self) -> None:
        nav_frame = ttk.Frame(self, padding=(12, 8))
        nav_frame.grid(row=2, column=0, sticky="nsew")

        # Three columns: [back btn] [spacer] [forward btn]
        nav_frame.columnconfigure(0, weight=1)
        nav_frame.columnconfigure(1, weight=0)   # fixed spacer
        nav_frame.columnconfigure(2, weight=1)
        nav_frame.rowconfigure(0, weight=1)

        self.go_back_button = ttk.Button(
            master=nav_frame,
            text="← Regresar",
            style="info.Outline.TButton",
            width=16,
        )
        self.go_back_button.grid(row=0, column=0, sticky="e", padx=(0, 10))

        # Invisible spacer label keeps the two buttons centred with a gap
        ttk.Label(nav_frame, text="", width=4).grid(row=0, column=1)

        self.continue_button = ttk.Button(
            master=nav_frame,
            text="Continuar →",
            style="info.TButton",
            width=16,
        )
        self.continue_button.grid(row=0, column=2, sticky="w", padx=(10, 0))
