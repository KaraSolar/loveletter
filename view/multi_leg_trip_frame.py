import ttkbootstrap as ttk


class MultiLegTrip(ttk.Frame):
    def __init__(self, master: ttk.Window, label_font_size: tuple):
        super().__init__(master)

        # ____________Initialize Variables __________
        self.label_font_size: tuple = label_font_size
        self.multi_leg_trip_var: ttk.BooleanVar = ttk.BooleanVar(value=False)

        # ____________FrameConfiguration_____________
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)   # Title row
        self.rowconfigure(1, weight=6)   # Buttons row
        self.rowconfigure(2, weight=1)   # Navigation row
        self.center_dynamic_frame = ttk.Frame(self)
        self.center_dynamic_frame.grid(row=1, column=0, sticky="nsew")
        self.center_dynamic_frame.columnconfigure(index=(0, 1), weight=1)
        self.center_dynamic_frame.rowconfigure(0, weight=1)

        self._build_title_frame()
        self._build_buttons_frame()
        self._build_navigation_frame()


    # _________________Methods_____________________________

    def _build_buttons_frame(self) -> None:

        # _____________Passenger Number Buttons____________

        self.not_multileg_trip_button: ttk.Button = ttk.Button(master=self.center_dynamic_frame,
                                                                text="Si",
                                                                style="info.TButton",
                                                                padding=(10, 20),
                                                                width=6,
                                                                command=lambda:self.multi_leg_trip_var.set(False)
                                                                )
        self.not_multileg_trip_button.grid(row=0, column=0, sticky="ew", padx=50)

        self.yes_multileg_trip_button: ttk.Button = ttk.Button(master=self.center_dynamic_frame,
                                                                style="info.TButton",
                                                                text="No",
                                                                padding=(10, 20),
                                                                width=6,
                                                                command=lambda:self.multi_leg_trip_var.set(True))
        self.yes_multileg_trip_button.grid(row=0, column=1, sticky="ew", padx=50)

    # _________________ Row 0 — Title _____________________________
    def _build_title_frame(self) -> None:
        title_frame = ttk.Frame(self, padding=(10, 8))
        title_frame.grid(row=0, column=0, sticky="nsew")
        title_frame.columnconfigure(0, weight=1)

        ttk.Label(
            title_frame,
            text="El viaje tiene destinos múltiples?",
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
