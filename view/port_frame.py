'''
This module contains PortFrame, part of the VIEW.
Reused for both departure and arrival port/finca selection.
Buttons are built dynamically via refresh() once a community is chosen.
'''

import ttkbootstrap as ttk
from functools import partial


class PortFrame(ttk.Frame):
    def __init__(self, master: ttk.Window, label_font_size: tuple,
                 communities_config: dict, community_var: ttk.StringVar, title: str):
        super().__init__(master)

        self.communities_config = communities_config
        self.community_var = community_var
        self.label_font_size = label_font_size
        self.title = title
        self.port_var: ttk.StringVar = ttk.StringVar(value="")
        self.buttons = {}
        self._last_built_community: str = None

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)   # Title row
        self.rowconfigure(1, weight=6)   # Buttons row
        self.rowconfigure(2, weight=1)   # Navigation row
        self.center_dynamic_frame = ttk.Frame(self)
        self.center_dynamic_frame.grid(row=1, column=0, sticky="nsew")
        self.center_dynamic_frame.columnconfigure(0, weight=1)
        self.center_dynamic_frame.rowconfigure(0, weight=1)

        self._build_title_frame()
        self._build_navigation_frame()

    # _________________ Row 0 — Title _____________________________
    def _build_title_frame(self) -> None:
        title_frame = ttk.Frame(self, padding=(10, 8))
        title_frame.grid(row=0, column=0, sticky="nsew")
        title_frame.columnconfigure(0, weight=1)

        ttk.Label(
            title_frame,
            text=self.title,
            font=(*self.label_font_size, "bold"),
            anchor="center",
        ).grid(row=0, column=0, sticky="ew")

    # _________________ Row 1 — Port Buttons (dynamic) ____________
    def refresh(self) -> None:
        current_community = self.community_var.get()
        if current_community == self._last_built_community:
            return
        for widget in self.center_dynamic_frame.winfo_children():
            widget.destroy()
        self.buttons.clear()
        self.port_var.set("")
        self._last_built_community = current_community
        ports = self.communities_config.get(current_community, [])
        self._build_buttons_frame(ports)

    def _build_buttons_frame(self, ports: list) -> None:
        COLS = 3

        buttons_frame = ttk.Frame(master=self.center_dynamic_frame)
        buttons_frame.grid(row=0, column=0, sticky="nsew")

        for c in range(COLS):
            buttons_frame.columnconfigure(c, weight=1)

        n_rows = -(-len(ports) // COLS)
        for r in range(n_rows):
            buttons_frame.rowconfigure(r, weight=0)
        buttons_frame.rowconfigure(n_rows, weight=1)

        for idx, port in enumerate(ports):
            row = idx // COLS
            col = idx % COLS
            btn = ttk.Button(
                master=buttons_frame,
                text=port,
                style="secondary.TButton",
                command=partial(self.select, port),
            )
            btn.grid(row=row, column=col, sticky="ew", padx=6, pady=6)
            self.buttons[port] = btn

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

        self.continue_button = ttk.Button(
            master=nav_frame,
            text="Continuar →",
            style="info.TButton",
            width=16,
        )
        self.continue_button.grid(row=0, column=2, sticky="w", padx=(10, 0))

    # _________________ Logic _____________________________________
    def select(self, port: str) -> None:
        self.port_var.set(port)
        self._update_selection()

    def _update_selection(self) -> None:
        current = self.port_var.get()
        for port, btn in self.buttons.items():
            style = "success.TButton" if port == current else "secondary.TButton"
            btn.configure(style=style)
