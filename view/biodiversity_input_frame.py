'''
This module contains BiodiversityInput, part of the VIEW.
Lets the user enter how many individuals of the selected species were sighted.
'''

import ttkbootstrap as ttk


class BiodiversityInput(ttk.Frame):
    def __init__(self, master: ttk.Window, label_font_size: tuple,
                 biodiversity_number_config: dict, biodiversity_var: ttk.StringVar):
        super().__init__(master)

        self.biodiversity_number_config = biodiversity_number_config
        self.max_sighting: int = biodiversity_number_config["max"]
        self.min_sighting: int = biodiversity_number_config["min"]
        self.label_font_size = label_font_size
        self.biodiversity_var = biodiversity_var
        self.sighting_count_var: ttk.IntVar = ttk.IntVar(value=self.min_sighting)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)   # Title row
        self.rowconfigure(1, weight=6)   # Buttons row
        self.rowconfigure(2, weight=1)   # Navigation row
        self.center_dynamic_frame = ttk.Frame(self)
        self.center_dynamic_frame.grid(row=1, column=0, sticky="nsew")
        self.center_dynamic_frame.columnconfigure((0, 1, 2), weight=1)
        self.center_dynamic_frame.rowconfigure(0, weight=1)

        self._build_title_frame()
        self._build_buttons_frame()
        self._build_navigation_frame()

    # _________________ Row 0 — Title _____________________________
    def _build_title_frame(self) -> None:
        title_frame = ttk.Frame(self, padding=(10, 8))
        title_frame.grid(row=0, column=0, sticky="nsew")
        title_frame.columnconfigure(0, weight=1)

        ttk.Label(
            title_frame,
            textvariable=self.biodiversity_var,
            font=(*self.label_font_size, "bold"),
            anchor="center",
        ).grid(row=0, column=0, sticky="ew")

    # _________________ Row 1 — Count Buttons _____________________
    def _build_buttons_frame(self) -> None:
        self.decrease_button = ttk.Button(
            master=self.center_dynamic_frame,
            text="Menos",
            style="info.TButton",
            padding=(10, 20),
            command=self._decrease,
        )
        self.decrease_button.grid(row=0, column=0, sticky="ew")

        self.count_label = ttk.Label(
            master=self.center_dynamic_frame,
            textvariable=self.sighting_count_var,
            font=("Digital-7", 50),
        )
        self.count_label.grid(row=0, column=1)

        self.increase_button = ttk.Button(
            master=self.center_dynamic_frame,
            text="Mas",
            style="info.TButton",
            padding=(10, 20),
            width=6,
            command=self._increase,
        )
        self.increase_button.grid(row=0, column=2, sticky="ew")

    # _________________ Row 2 — Navigation _______________________
    def _build_navigation_frame(self) -> None:
        nav_frame = ttk.Frame(self, padding=(12, 8))
        nav_frame.grid(row=2, column=0, sticky="nsew")

        nav_frame.columnconfigure(0, weight=1)
        nav_frame.columnconfigure(1, weight=0)
        nav_frame.columnconfigure(2, weight=1)
        nav_frame.rowconfigure(0, weight=1)

        self.go_back_button = ttk.Button(
            master=nav_frame,
            text="← Regresar",
            style="info.Outline.TButton",
            width=16,
        )
        self.go_back_button.grid(row=0, column=0, sticky="e", padx=(0, 10))

        ttk.Label(nav_frame, text="", width=4).grid(row=0, column=1)

        self.register_button = ttk.Button(
            master=nav_frame,
            text="Registrar →",
            style="info.TButton",
            width=16,
        )
        self.register_button.grid(row=0, column=2, sticky="w", padx=(10, 0))

    # _________________ Logic _____________________________________
    def refresh(self) -> None:
        self.sighting_count_var.set(self.min_sighting)

    def _decrease(self) -> None:
        n = self.sighting_count_var.get()
        if n > self.min_sighting:
            self.sighting_count_var.set(n - 1)

    def _increase(self) -> None:
        n = self.sighting_count_var.get()
        if n < self.max_sighting:
            self.sighting_count_var.set(n + 1)
