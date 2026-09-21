"""One ordering screen used for every table and takeaway slot
(replaces the nine copy-pasted 'Ordering Page' files)."""
import tkinter as tk
from datetime import datetime
from tkinter import messagebox, ttk

from .. import config
from ..db import OrderError
from ..pricing import format_money
from . import theme
from .app import header

SLOT_LABELS = dict(config.SLOTS)
MENU_COLUMNS = 3


class OrderScreen(ttk.Frame):
    def __init__(self, parent, app, slot):
        super().__init__(parent)
        self.app, self.db, self.slot = app, app.db, slot
        existing = self.db.active_order(slot)
        self.order_id = existing["id"] if existing else None  # created on first item

        header(self, app, SLOT_LABELS[slot], back=self.go_back, back_label="All tables")

        body = ttk.Frame(self, padding=16)
        body.pack(fill="both", expand=True)
        body.columnconfigure(0, weight=2, uniform="col")
        body.columnconfigure(1, weight=3, uniform="col")
        body.rowconfigure(0, weight=1)

        self.build_order_panel(body).grid(row=0, column=0, sticky="nsew", padx=(0, 16))
        self.build_menu_panel(body).grid(row=0, column=1, sticky="nsew")

        self.message = ttk.Label(self, text="", style="Error.TLabel", padding=(16, 0, 16, 12))
        self.message.pack(fill="x")
        self.refresh()

    # ---------- layout ----------

    def build_order_panel(self, parent):
        panel = ttk.Frame(parent, style="Panel.TFrame", padding=16)
        panel.columnconfigure(0, weight=1)
        panel.rowconfigure(2, weight=1)

        top = ttk.Frame(panel, style="Panel.TFrame")
        top.grid(row=0, column=0, sticky="ew")
        required = " (required for takeaway)" if self.slot.startswith("TK") else " (optional)"
        ttk.Label(top, text="Customer name" + required, style="PanelMuted.TLabel").pack(anchor="w")
        self.name_var = tk.StringVar()
        name_entry = ttk.Entry(top, textvariable=self.name_var, font=theme.F_BODY)
        name_entry.pack(fill="x", pady=(2, 8))
        name_entry.bind("<FocusOut>", lambda e: self.save_name())
        name_entry.bind("<Return>", lambda e: self.save_name())

        self.status_label = ttk.Label(panel, text="", style="PanelMuted.TLabel")
        self.status_label.grid(row=1, column=0, sticky="w", pady=(0, 6))

        cols = ("item", "qty", "price", "line")
        tree_frame = ttk.Frame(panel, style="Panel.TFrame")
        tree_frame.grid(row=2, column=0, sticky="nsew")
        self.tree = ttk.Treeview(tree_frame, columns=cols, show="headings", selectmode="browse")
        for col, text, width, anchor in [("item", "Item", 180, "w"), ("qty", "Qty", 50, "center"),
                                         ("price", "Each", 80, "e"), ("line", "Total", 90, "e")]:
            self.tree.heading(col, text=text, anchor=anchor)
            self.tree.column(col, width=width, anchor=anchor, stretch=(col == "item"))
        scroll = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

        qty = ttk.Frame(panel, style="Panel.TFrame")
        qty.grid(row=3, column=0, sticky="ew", pady=8)
        ttk.Button(qty, text="−", style="Qty.TButton", width=3,
                   command=lambda: self.change_selected(-1)).pack(side="left")
        ttk.Button(qty, text="+", style="Qty.TButton", width=3,
                   command=lambda: self.change_selected(+1)).pack(side="left", padx=6)
        ttk.Button(qty, text="Remove item", command=self.remove_selected).pack(side="left")
        ttk.Button(qty, text="Void order", style="Danger.TButton", command=self.void).pack(side="right")

        adj = ttk.Frame(panel, style="Panel.TFrame")
        adj.grid(row=4, column=0, sticky="ew")
        self.discount_var = tk.BooleanVar()
        self.surcharge_var = tk.BooleanVar()
        ttk.Checkbutton(adj, text=f"{config.DISCOUNT_PERCENT}% discount",
                        variable=self.discount_var, command=self.save_adjustments).pack(side="left")
        ttk.Checkbutton(adj, text=f"{config.SURCHARGE_PERCENT}% surcharge",
                        variable=self.surcharge_var, command=self.save_adjustments).pack(side="left", padx=16)

        totals = ttk.Frame(panel, style="Panel.TFrame")
        totals.grid(row=5, column=0, sticky="ew", pady=(10, 6))
        totals.columnconfigure(1, weight=1)
        self.total_labels = {}
        for r, key in enumerate(["Subtotal", "Discount", "Surcharge"]):
            ttk.Label(totals, text=key, style="PanelMuted.TLabel").grid(row=r, column=0, sticky="w")
            self.total_labels[key] = ttk.Label(totals, text="", style="Panel.TLabel")
            self.total_labels[key].grid(row=r, column=1, sticky="e")
        ttk.Label(totals, text="Total", style="PanelTitle.TLabel").grid(row=3, column=0, sticky="w", pady=(6, 0))
        self.total_labels["Total"] = ttk.Label(totals, text="", style="Total.TLabel")
        self.total_labels["Total"].grid(row=3, column=1, sticky="e", pady=(6, 0))

        actions = ttk.Frame(panel, style="Panel.TFrame")
        actions.grid(row=6, column=0, sticky="ew", pady=(8, 0))
        actions.columnconfigure(0, weight=1, uniform="act")
        actions.columnconfigure(1, weight=1, uniform="act")
        ttk.Button(actions, text="Send to kitchen", style="Accent.TButton",
                   command=self.send).grid(row=0, column=0, sticky="ew", padx=(0, 4))
        ttk.Button(actions, text="Complete order", style="Primary.TButton",
                   command=self.complete).grid(row=0, column=1, sticky="ew", padx=(4, 0))
        return panel

    def build_menu_panel(self, parent):
        panel = ttk.Frame(parent)
        ttk.Label(panel, text="Menu", style="Title.TLabel").pack(anchor="w", pady=(0, 8))
        grid = ttk.Frame(panel)
        grid.pack(fill="both", expand=True)
        items = self.db.menu()
        rows = max(1, -(-len(items) // MENU_COLUMNS))
        for c in range(MENU_COLUMNS):
            grid.columnconfigure(c, weight=1, uniform="menu")
        for r in range(rows):
            grid.rowconfigure(r, weight=1, uniform="menu")  # tiles share the height, so the menu always fits
        for i, item in enumerate(items):
            ttk.Button(grid, text=f"{item['name']}\n{format_money(item['price_cents'])}",
                       style="Tile.TButton",
                       command=lambda mid=item["id"]: self.add(mid)).grid(
                row=i // MENU_COLUMNS, column=i % MENU_COLUMNS, sticky="nsew", padx=4, pady=4)
        return panel

    # ---------- actions ----------

    def run(self, action, *args):
        """Run a database change; show rule violations instead of crashing."""
        try:
            action(*args)
            self.message.configure(text="")
            return True
        except OrderError as e:
            self.message.configure(text=str(e))
            return False
        finally:
            self.refresh()

    def ensure_order(self):
        if self.order_id is None:
            self.order_id = self.db.get_or_create_active_order(self.slot, self.app.user["id"])
            if self.name_var.get().strip():
                self.db.set_customer_name(self.order_id, self.name_var.get())
            if self.discount_var.get() or self.surcharge_var.get():
                self.db.set_adjustments(self.order_id, self.discount_var.get(), self.surcharge_var.get())
        return self.order_id

    def add(self, menu_item_id):
        self.run(lambda: self.db.add_item(self.ensure_order(), menu_item_id))

    def selected_line(self):
        sel = self.tree.selection()
        if not sel:
            self.message.configure(text="Select an item on the order first.")
            return None
        return int(sel[0])

    def change_selected(self, delta):
        line = self.selected_line()
        if line is not None:
            self.run(self.db.change_quantity, line, delta)

    def remove_selected(self):
        line = self.selected_line()
        if line is not None:
            self.run(self.db.remove_line, line)

    def save_adjustments(self):
        if self.order_id is None:
            return self.refresh()  # remembered and applied when the first item is added
        self.run(self.db.set_adjustments, self.order_id, self.discount_var.get(), self.surcharge_var.get())

    def save_name(self):
        if self.order_id is not None:
            self.run(self.db.set_customer_name, self.order_id, self.name_var.get())

    def send(self):
        if self.order_id is None:
            return self.message.configure(text="Add at least one item before sending to the kitchen.")
        self.save_name()
        if self.run(self.db.send_to_kitchen, self.order_id):
            self.message.configure(text="")
            self.status_label.configure(text=self.status_text())

    def complete(self):
        if self.order_id is None:
            return self.message.configure(text="Add at least one item before completing the order.")
        self.save_name()
        total = format_money(self.db.order(self.order_id)["total_cents"])
        if not messagebox.askyesno("Complete order",
                                   f"Complete this order for {total}?\nIt can't be changed afterwards.",
                                   parent=self):
            return
        if self.run(self.db.complete, self.order_id):
            self.app.show(_main_menu())

    def void(self):
        if self.order_id is None or not self.db.items(self.order_id):
            if self.order_id is not None:
                self.db.void(self.order_id)
            return self.app.show(_main_menu())
        if messagebox.askyesno("Void order",
                               "Void this order? It will be kept in the reports as voided "
                               "and won't count towards revenue.", icon="warning", parent=self):
            if self.run(self.db.void, self.order_id):
                self.app.show(_main_menu())

    def go_back(self):
        if self.order_id is not None:
            self.save_name()
            # An order with nothing on it shouldn't keep the table marked as busy.
            if not self.db.items(self.order_id) and self.db.order(self.order_id)["status"] == "open":
                self.db.void(self.order_id)
        self.app.show(_main_menu())

    # ---------- display ----------

    def status_text(self):
        if self.order_id is None:
            return "New order. Tap a menu item to start."
        o = self.db.order(self.order_id)
        if o["status"] == "sent":
            sent = datetime.fromisoformat(o["sent_at"]).strftime("%H:%M")
            return f"Sent to kitchen at {sent}. Items added now need sending again."
        opened = datetime.fromisoformat(o["created_at"]).strftime("%H:%M")
        return f"Order opened at {opened}."

    def refresh(self):
        selected = self.tree.selection()
        self.tree.delete(*self.tree.get_children())
        order = self.db.order(self.order_id) if self.order_id else None
        if order is None:
            self.order_id = None
            values = dict(subtotal_cents=0, discount_cents=0, surcharge_cents=0, total_cents=0)
        else:
            values = order
            for line in self.db.items(self.order_id):
                self.tree.insert("", "end", iid=str(line["id"]), values=(
                    line["name"], line["quantity"], format_money(line["unit_price_cents"]),
                    format_money(line["unit_price_cents"] * line["quantity"])))
            if not self.name_var.get() and order["customer_name"]:
                self.name_var.set(order["customer_name"])
            self.discount_var.set(bool(order["discount_applied"]))
            self.surcharge_var.set(bool(order["surcharge_applied"]))
        for iid in selected:
            if self.tree.exists(iid):
                self.tree.selection_set(iid)
        self.total_labels["Subtotal"].configure(text=format_money(values["subtotal_cents"]))
        self.total_labels["Discount"].configure(text="−" + format_money(values["discount_cents"]))
        self.total_labels["Surcharge"].configure(text=format_money(values["surcharge_cents"]))
        self.total_labels["Total"].configure(text=format_money(values["total_cents"]))
        self.status_label.configure(text=self.status_text())


def _main_menu():
    from .main_menu import MainMenu
    return MainMenu
