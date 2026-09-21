"""Daily reports (replaces the old 'Functionality Page').

Totals are per real calendar day, using the time each order was closed."""
import tkinter as tk
from datetime import date, datetime, timedelta
from tkinter import ttk

from .. import config
from ..pricing import format_money
from . import theme
from .app import header

SLOT_LABELS = dict(config.SLOTS)
COLUMNS = [  # id, heading, width, anchor, sort key
    ("time", "Closed", 80, "w", lambda o: o["closed_at"]),
    ("slot", "Table", 110, "w", lambda o: o["slot"]),
    ("customer", "Customer", 160, "w", lambda o: o["customer_name"].lower()),
    ("items", "Items", 360, "w", lambda o: o["_items"]),
    ("status", "Status", 100, "w", lambda o: o["status"]),
    ("total", "Total", 100, "e", lambda o: o["total_cents"]),
]


class ReportsScreen(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app, self.db = app, app.db
        self.day = date.today()
        self.sort_col, self.sort_desc = "time", False
        self.rows = []

        header(self, app, "Reports", back=self.go_back, back_label="All tables")
        body = ttk.Frame(self, padding=20)
        body.pack(fill="both", expand=True)

        controls = ttk.Frame(body)
        controls.pack(fill="x")
        ttk.Button(controls, text="Previous day", command=lambda: self.move(-1)).pack(side="left")
        self.day_label = ttk.Label(controls, text="", style="Title.TLabel", width=16, anchor="center")
        self.day_label.pack(side="left", padx=12)
        self.next_btn = ttk.Button(controls, text="Next day", command=lambda: self.move(1))
        self.next_btn.pack(side="left")
        ttk.Button(controls, text="Today", command=self.go_today).pack(side="left", padx=(8, 0))

        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", lambda *a: self.load())
        search = ttk.Entry(controls, textvariable=self.search_var, width=24, font=theme.F_BODY)
        search.pack(side="right")
        ttk.Label(controls, text="Customer name", style="Muted.TLabel").pack(side="right", padx=8)

        stats = ttk.Frame(body)
        stats.pack(fill="x", pady=16)
        self.stats = {}
        for i, (key, label) in enumerate([("revenue", "Revenue"), ("completed", "Completed orders"),
                                          ("discounts", "Discounts given"), ("surcharges", "Surcharges"),
                                          ("voided", "Voided orders")]):
            stats.columnconfigure(i, weight=1, uniform="stat")
            card = ttk.Frame(stats, style="Panel.TFrame", padding=14)
            card.grid(row=0, column=i, sticky="nsew", padx=(0 if i == 0 else 8, 0))
            ttk.Label(card, text=label, style="PanelMuted.TLabel").pack(anchor="w")
            self.stats[key] = ttk.Label(card, text="", style="Stat.TLabel")
            self.stats[key].pack(anchor="w")

        table = ttk.Frame(body, style="Panel.TFrame")
        table.pack(fill="both", expand=True)
        self.tree = ttk.Treeview(table, columns=[c[0] for c in COLUMNS], show="headings")
        for cid, text, width, anchor, _ in COLUMNS:
            self.tree.heading(cid, text=text, anchor=anchor, command=lambda c=cid: self.sort_by(c))
            self.tree.column(cid, width=width, anchor=anchor, stretch=(cid == "items"))
        scroll = ttk.Scrollbar(table, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")
        self.tree.bind("<Double-1>", self.show_detail)
        self.tree.bind("<Return>", self.show_detail)
        self.empty = ttk.Label(body, text="", style="Muted.TLabel")
        self.empty.pack(anchor="w", pady=(8, 0))
        ttk.Label(body, text="Click a column heading to sort. Double-click an order to see its items.",
                  style="Muted.TLabel").pack(anchor="w")

        search.focus_set()
        self.load()

    def move(self, days):
        self.day = min(date.today(), self.day + timedelta(days=days))
        self.load()

    def go_today(self):
        self.day = date.today()
        self.load()

    def sort_by(self, col):
        self.sort_desc = not self.sort_desc if col == self.sort_col else col == "total"
        self.sort_col = col
        self.render()

    def load(self):
        self.day_label.configure(text=self.day.strftime("%a %d %b %Y"))
        self.next_btn.state(["disabled"] if self.day >= date.today() else ["!disabled"])
        summary = self.db.daily_summary(self.day)
        for key in ("revenue", "discounts", "surcharges"):
            self.stats[key].configure(text=format_money(summary[key]))
        for key in ("completed", "voided"):
            self.stats[key].configure(text=str(summary[key]))

        self.rows = []
        for o in self.db.closed_orders_on(self.day, self.search_var.get()):
            row = dict(o)
            row["_lines"] = self.db.items(o["id"])
            row["_items"] = ", ".join(f"{l['quantity']}× {l['name']}" for l in row["_lines"])
            self.rows.append(row)
        self.render()

    def render(self):
        key = next(c[4] for c in COLUMNS if c[0] == self.sort_col)
        self.tree.delete(*self.tree.get_children())
        for o in sorted(self.rows, key=key, reverse=self.sort_desc):
            self.tree.insert("", "end", iid=str(o["id"]), values=(
                datetime.fromisoformat(o["closed_at"]).strftime("%H:%M"),
                SLOT_LABELS.get(o["slot"], o["slot"]),
                o["customer_name"] or "—",
                o["_items"],
                "Voided" if o["status"] == "void" else "Completed",
                format_money(o["total_cents"]),
            ))
        for cid, text, *_ in COLUMNS:
            arrow = (" ▼" if self.sort_desc else " ▲") if cid == self.sort_col else ""
            self.tree.heading(cid, text=text + arrow)
        if self.rows:
            self.empty.configure(text="")
        elif self.search_var.get().strip():
            self.empty.configure(text="No orders match that name on this day.")
        else:
            self.empty.configure(text="No completed or voided orders on this day.")

    def show_detail(self, _event=None):
        sel = self.tree.selection()
        if not sel:
            return
        o = next(r for r in self.rows if r["id"] == int(sel[0]))
        win = tk.Toplevel(self)
        win.title(f"Order #{o['id']}")
        win.configure(bg=theme.PANEL)
        win.transient(self.winfo_toplevel())
        frame = ttk.Frame(win, style="Panel.TFrame", padding=20)
        frame.pack(fill="both", expand=True)
        frame.columnconfigure(1, weight=1)
        title = f"Order #{o['id']}, {SLOT_LABELS.get(o['slot'], o['slot'])}"
        ttk.Label(frame, text=title, style="PanelTitle.TLabel").grid(row=0, column=0, columnspan=2, sticky="w")
        closed = datetime.fromisoformat(o["closed_at"]).strftime("%d %b %Y %H:%M")
        state = "Voided" if o["status"] == "void" else "Completed"
        ttk.Label(frame, text=f"{state} {closed}. Customer: {o['customer_name'] or 'not given'}",
                  style="PanelMuted.TLabel").grid(row=1, column=0, columnspan=2, sticky="w", pady=(0, 10))
        r = 2
        for line in o["_lines"]:
            ttk.Label(frame, text=f"{line['quantity']}× {line['name']}", style="Panel.TLabel").grid(row=r, column=0, sticky="w")
            ttk.Label(frame, text=format_money(line["unit_price_cents"] * line["quantity"]),
                      style="Panel.TLabel").grid(row=r, column=1, sticky="e")
            r += 1
        rows = [("Subtotal", o["subtotal_cents"])]
        if o["discount_applied"]:
            rows.append((f"Discount ({o['discount_percent']}%)", -o["discount_cents"]))
        if o["surcharge_applied"]:
            rows.append((f"Surcharge ({o['surcharge_percent']}%)", o["surcharge_cents"]))
        ttk.Separator(frame).grid(row=r, column=0, columnspan=2, sticky="ew", pady=8)
        r += 1
        for label, cents in rows:
            ttk.Label(frame, text=label, style="PanelMuted.TLabel").grid(row=r, column=0, sticky="w")
            ttk.Label(frame, text=format_money(cents), style="Panel.TLabel").grid(row=r, column=1, sticky="e")
            r += 1
        ttk.Label(frame, text="Total", style="PanelTitle.TLabel").grid(row=r, column=0, sticky="w", pady=(6, 0))
        ttk.Label(frame, text=format_money(o["total_cents"]), style="PanelTitle.TLabel").grid(row=r, column=1, sticky="e", pady=(6, 0))
        ttk.Button(frame, text="Close", command=win.destroy).grid(row=r + 1, column=0, columnspan=2, pady=(16, 0))
        win.minsize(360, 0)

    def go_back(self):
        from .main_menu import MainMenu
        self.app.show(MainMenu)
