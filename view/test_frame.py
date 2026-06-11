import ttkbootstrap as ttk


class TestFrame(ttk.Frame):
    def __init__(self, master: ttk.Window, label_font_size: tuple):
        super().__init__(master)

        self.label_font_size: tuple = label_font_size
        self.test_var: ttk.BooleanVar = ttk.BooleanVar(value=False)

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

    # _________________ Row 0 — Title _____________________________
    def _build_title_frame(self) -> None:
        title_frame = ttk.Frame(self, padding=(10, 8))
        title_frame.grid(row=0, column=0, sticky="nsew")
        title_frame.columnconfigure(0, weight=1)

        ttk.Label(
            title_frame,
            text="Viaje de Prueba",
            font=(*self.label_font_size, "bold"),
            anchor="center",
        ).grid(row=0, column=0, sticky="ew")

    # _________________ Row 1 — Si / No Buttons ___________________
    def _build_buttons_frame(self) -> None:
        self.si_button = ttk.Button(
            master=self.center_dynamic_frame,
            text="Si",
            style="secondary.TButton",
            padding=(10, 20),
            width=6,
            command=lambda: self.select(True),
        )
        self.si_button.grid(row=0, column=0, sticky="ew", padx=50)

        self.no_button = ttk.Button(
            master=self.center_dynamic_frame,
            text="No",
            style="secondary.TButton",
            padding=(10, 20),
            width=6,
            command=lambda: self.select(False),
        )
        self.no_button.grid(row=0, column=1, sticky="ew", padx=50)
        self._update_selection()

    # _________________ Row 2 — Navigation _______________________
    def _build_navigation_frame(self) -> None:
        nav_frame = ttk.Frame(self, padding=(12, 8))
        nav_frame.grid(row=2, column=0, sticky="nsew")
        nav_frame.columnconfigure(0, weight=1)
        nav_frame.rowconfigure(0, weight=1)

        self.go_back_button = ttk.Button(
            master=nav_frame,
            text="← Regresar",
            style="info.Outline.TButton",
            width=16,
        )
        self.go_back_button.grid(row=0, column=0, sticky="e", padx=(0, 10))

    # _________________ Logic _____________________________________
    def select(self, value: bool) -> None:
        self.test_var.set(value)
        self._update_selection()

    def _update_selection(self) -> None:
        current = self.test_var.get()
        self.si_button.configure(style="success.TButton" if current else "secondary.TButton")
        self.no_button.configure(style="success.TButton" if not current else "secondary.TButton")
