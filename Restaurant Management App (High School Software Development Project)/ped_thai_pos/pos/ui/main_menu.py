from tkinter import ttk

from .. import config
from ..pricing import format_money
from .app import header


class MainMenu(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        bar = header(self, app, config.APP_NAME)
        for text, style, cmd in [("Sign out", "Header.TButton", app.logout),
                                 ("Reports", "Header.TButton", self.open_reports)]:
            ttk.Button(bar, text=text, style=style, command=cmd).pack(side="right", padx=(0, 16))

        body = ttk.Frame(self, padding=24)
        body.pack(fill="both", expand=True)
        active = app.db.active_orders_by_slot()

        tables = [s for s in config.SLOTS if s[0].startswith("T") and not s[0].startswith("TK")]
        takeaways = [s for s in config.SLOTS if s[0].startswith("TK")]
        self.section(body, "Tables", tables, active, columns=3)
        self.section(body, "Takeaway", takeaways, active, columns=3)

        legend = ttk.Frame(body)
        legend.pack(fill="x", pady=(12, 0))
        ttk.Label(legend, text="White: available.  Green: order in progress.  Yellow: sent to kitchen.",
                  style="Muted.TLabel").pack(side="left")

    def section(self, parent, title, slots, active, columns):
        ttk.Label(parent, text=title, style="Title.TLabel").pack(anchor="w", pady=(8, 8))
        grid = ttk.Frame(parent)
        grid.pack(fill="x", pady=(0, 16))
        for c in range(columns):
            grid.columnconfigure(c, weight=1, uniform="slot")
        for i, (slot, label) in enumerate(slots):
            order = active.get(slot)
            if order is None:
                text, style = f"{label}\nAvailable", "SlotFree.TButton"
            elif order["status"] == "sent":
                text, style = f"{label}\nSent to kitchen, {format_money(order['total_cents'])}", "SlotSent.TButton"
            else:
                text, style = f"{label}\nIn progress, {format_money(order['total_cents'])}", "SlotOpen.TButton"
            ttk.Button(grid, text=text, style=style,
                       command=lambda s=slot: self.open_slot(s)).grid(
                row=i // columns, column=i % columns, sticky="nsew", padx=6, pady=6)

    def open_slot(self, slot):
        from .ordering import OrderScreen
        self.app.show(OrderScreen, slot=slot)

    def open_reports(self):
        from .reports import ReportsScreen
        self.app.show(ReportsScreen)
