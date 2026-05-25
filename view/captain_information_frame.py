'''
This module contains the class CaptainInformation, part of the VIEW.
'''

import ttkbootstrap as ttk
from functools import partial


class CaptainInformation(ttk.Frame):
    def __init__(self, master: ttk.Window, label_font_size: tuple, captains_config: list):
        super().__init__(master)

        # ____________Initialize Variables __________
        self.captains_config = captains_config
        self.label_font_size: tuple = label_font_size
        self.captains_var: ttk.StringVar = ttk.StringVar(value=None)
        self.buttons = {}

        # ____________ Frame Configuration (3-row grid) _____________
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)   # Title row
        self.rowconfigure(1, weight=6)   # Buttons row
        self.rowconfigure(2, weight=1)   # Navigation row
        self.center_dynamic_frame = ttk.Frame(self)
        self.center_dynamic_frame.grid(row=1, column=0, sticky="nsew")
        self.center_dynamic_frame.columnconfigure(0, weight=1)
        self.center_dynamic_frame.rowconfigure(0, weight=1)   # Title row

        self._build_title_frame()
        self._build_buttons_frame()
        self._build_navigation_frame()

    # _________________ Row 0 — Title _____________________________
    def _build_title_frame(self) -> None:
        title_frame = ttk.Frame(self)
        title_frame.grid(row=0, column=0, sticky="nsew")
        title_frame.columnconfigure(0, weight=1)

        ttk.Label(
            title_frame,
            text="Seleccionar Capitán",
            font=(*self.label_font_size, "bold"),
            anchor="center",
        ).grid(row=0, column=0, sticky="ew")

    # _________________ Row 1 — Captain Buttons ___________________
    def _build_buttons_frame(self) -> None:
        COLS = 3  # buttons per row; change to 4 for a 4-column grid

        buttons_frame = ttk.Frame(master=self.center_dynamic_frame)
        buttons_frame.grid(row=0,column=0,sticky="nsew")

        # Make every column and row inside this frame expand evenly
        for c in range(COLS):
            buttons_frame.columnconfigure(c, weight=1)

        n_rows = -(-len(self.captains_config) // COLS)  # ceiling division
        # Rows do NOT expand — buttons keep a natural height regardless of count
        for r in range(n_rows):
            buttons_frame.rowconfigure(r, weight=0)

        # Extra empty row at the bottom absorbs leftover space
        buttons_frame.rowconfigure(n_rows, weight=1)

        for idx, opt in enumerate(self.captains_config):
            row = idx // COLS
            col = idx % COLS

            btn = ttk.Button(
                master=buttons_frame,
                text=opt,
                style="secondary.TButton",
                command=partial(self.select, opt),
            )
            # Stretch horizontally to fill the column, but keep natural height
            btn.grid(row=row, column=col, sticky="ew", padx=6, pady=6)
            self.buttons[opt] = btn

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

    # _________________ Logic _____________________________________
    def select(self, opt: str) -> None:
        self.captains_var.set(opt)
        self._update_selection()
        print(self.captains_var.get())

    def _update_selection(self) -> None:
        current = self.captains_var.get()
        for opt, btn in self.buttons.items():
            style = "success.TButton" if opt == current else "secondary.TButton"
            btn.configure(style=style)
