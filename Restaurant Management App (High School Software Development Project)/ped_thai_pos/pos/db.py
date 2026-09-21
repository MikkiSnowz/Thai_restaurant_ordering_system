"""SQLite storage for users, the menu, and orders.

Every change is written immediately inside a transaction, so an order
survives the app being closed or crashing mid-service.
"""
import sqlite3
from datetime import date, datetime
from pathlib import Path

from . import auth, config
from .pricing import calculate_totals

ACTIVE_STATUSES = ("open", "sent")

SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
    id          INTEGER PRIMARY KEY,
    username    TEXT NOT NULL UNIQUE COLLATE NOCASE,
    pw_hash     TEXT NOT NULL,
    role        TEXT NOT NULL DEFAULT 'staff' CHECK (role IN ('admin', 'staff')),
    active      INTEGER NOT NULL DEFAULT 1,
    created_at  TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS menu_items (
    id           INTEGER PRIMARY KEY,
    name         TEXT NOT NULL UNIQUE,
    price_cents  INTEGER NOT NULL CHECK (price_cents >= 0),
    category     TEXT NOT NULL,
    sort_order   INTEGER NOT NULL DEFAULT 0,
    active       INTEGER NOT NULL DEFAULT 1
);

CREATE TABLE IF NOT EXISTS orders (
    id                 INTEGER PRIMARY KEY,
    slot               TEXT NOT NULL,
    customer_name      TEXT NOT NULL DEFAULT '',
    status             TEXT NOT NULL DEFAULT 'open'
                       CHECK (status IN ('open', 'sent', 'completed', 'void')),
    discount_applied   INTEGER NOT NULL DEFAULT 0,
    surcharge_applied  INTEGER NOT NULL DEFAULT 0,
    discount_percent   INTEGER NOT NULL,
    surcharge_percent  INTEGER NOT NULL,
    subtotal_cents     INTEGER NOT NULL DEFAULT 0,
    discount_cents     INTEGER NOT NULL DEFAULT 0,
    surcharge_cents    INTEGER NOT NULL DEFAULT 0,
    total_cents        INTEGER NOT NULL DEFAULT 0,
    created_by         INTEGER REFERENCES users(id),
    created_at         TEXT NOT NULL,
    sent_at            TEXT,
    closed_at          TEXT
);

-- Only one active (open or sent) order per table/takeaway slot.
CREATE UNIQUE INDEX IF NOT EXISTS one_active_order_per_slot
    ON orders(slot) WHERE status IN ('open', 'sent');

CREATE INDEX IF NOT EXISTS orders_closed_at ON orders(closed_at);

CREATE TABLE IF NOT EXISTS order_items (
    id                INTEGER PRIMARY KEY,
    order_id          INTEGER NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
    menu_item_id      INTEGER NOT NULL REFERENCES menu_items(id),
    name              TEXT NOT NULL,          -- snapshot, so old orders keep old names
    unit_price_cents  INTEGER NOT NULL,       -- snapshot, so price changes don't rewrite history
    quantity          INTEGER NOT NULL CHECK (quantity > 0),
    UNIQUE (order_id, menu_item_id)
);
"""


class OrderError(Exception):
    """A business rule stopped the change. The message is safe to show to staff."""


def now() -> str:
    return datetime.now().isoformat(timespec="seconds")


class Database:
    def __init__(self, path: Path | str = config.DB_PATH):
        if str(path) != ":memory:":
            Path(path).parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(str(path))
        self.conn.row_factory = sqlite3.Row
        self.conn.execute("PRAGMA foreign_keys = ON")
        self.conn.execute("PRAGMA journal_mode = WAL")
        self.conn.executescript(SCHEMA)
        self._seed_menu()

    def close(self):
        self.conn.close()

    # ---------- users ----------

    def user_count(self) -> int:
        return self.conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]

    def create_user(self, username: str, password: str, role: str = "staff") -> int:
        username = username.strip()
        if not username:
            raise OrderError("Enter a username.")
        problem = auth.password_problem(password)
        if problem:
            raise OrderError(problem)
        try:
            with self.conn:
                cur = self.conn.execute(
                    "INSERT INTO users (username, pw_hash, role, created_at) VALUES (?, ?, ?, ?)",
                    (username, auth.hash_password(password), role, now()),
                )
        except sqlite3.IntegrityError:
            raise OrderError(f"The username '{username}' is already taken.") from None
        return cur.lastrowid

    def authenticate(self, username: str, password: str):
        row = self.conn.execute(
            "SELECT * FROM users WHERE username = ? AND active = 1", (username.strip(),)
        ).fetchone()
        if row and auth.verify_password(password, row["pw_hash"]):
            return row
        return None

    # ---------- menu ----------

    def _seed_menu(self):
        if self.conn.execute("SELECT COUNT(*) FROM menu_items").fetchone()[0]:
            return
        with self.conn:
            self.conn.executemany(
                "INSERT INTO menu_items (name, price_cents, category, sort_order) VALUES (?, ?, ?, ?)",
                [(n, p, c, i) for i, (n, p, c) in enumerate(config.DEFAULT_MENU)],
            )

    def menu(self):
        return self.conn.execute(
            "SELECT * FROM menu_items WHERE active = 1 ORDER BY sort_order, name"
        ).fetchall()

    # ---------- orders ----------

    def order(self, order_id: int):
        return self.conn.execute("SELECT * FROM orders WHERE id = ?", (order_id,)).fetchone()

    def active_order(self, slot: str):
        return self.conn.execute(
            "SELECT * FROM orders WHERE slot = ? AND status IN ('open', 'sent')", (slot,)
        ).fetchone()

    def active_orders_by_slot(self) -> dict:
        rows = self.conn.execute(
            "SELECT * FROM orders WHERE status IN ('open', 'sent')"
        ).fetchall()
        return {r["slot"]: r for r in rows}

    def items(self, order_id: int):
        return self.conn.execute(
            "SELECT * FROM order_items WHERE order_id = ? ORDER BY id", (order_id,)
        ).fetchall()

    def get_or_create_active_order(self, slot: str, user_id: int | None) -> int:
        existing = self.active_order(slot)
        if existing:
            return existing["id"]
        with self.conn:
            cur = self.conn.execute(
                """INSERT INTO orders (slot, discount_percent, surcharge_percent, created_by, created_at)
                   VALUES (?, ?, ?, ?, ?)""",
                (slot, config.DISCOUNT_PERCENT, config.SURCHARGE_PERCENT, user_id, now()),
            )
        return cur.lastrowid

    def _require_editable(self, order_id: int):
        row = self.order(order_id)
        if row is None:
            raise OrderError("That order no longer exists.")
        if row["status"] not in ACTIVE_STATUSES:
            raise OrderError(f"This order is {row['status']} and can't be changed.")
        return row

    def _recalculate(self, order_id: int):
        """Recompute stored totals. Call inside an open transaction."""
        row = self.order(order_id)
        lines = [(i["unit_price_cents"], i["quantity"]) for i in self.items(order_id)]
        t = calculate_totals(
            lines,
            bool(row["discount_applied"]),
            bool(row["surcharge_applied"]),
            row["discount_percent"],
            row["surcharge_percent"],
        )
        self.conn.execute(
            """UPDATE orders SET subtotal_cents = ?, discount_cents = ?,
               surcharge_cents = ?, total_cents = ? WHERE id = ?""",
            (t.subtotal, t.discount, t.surcharge, t.total, order_id),
        )

    def item_count(self, order_id: int) -> int:
        return self.conn.execute(
            "SELECT COALESCE(SUM(quantity), 0) FROM order_items WHERE order_id = ?", (order_id,)
        ).fetchone()[0]

    def add_item(self, order_id: int, menu_item_id: int):
        self._require_editable(order_id)
        if self.item_count(order_id) >= config.MAX_ITEMS_PER_ORDER:
            raise OrderError(
                f"An order can have at most {config.MAX_ITEMS_PER_ORDER} items."
            )
        item = self.conn.execute(
            "SELECT * FROM menu_items WHERE id = ? AND active = 1", (menu_item_id,)
        ).fetchone()
        if item is None:
            raise OrderError("That menu item is no longer available.")
        with self.conn:
            self.conn.execute(
                """INSERT INTO order_items (order_id, menu_item_id, name, unit_price_cents, quantity)
                   VALUES (?, ?, ?, ?, 1)
                   ON CONFLICT (order_id, menu_item_id) DO UPDATE SET quantity = quantity + 1""",
                (order_id, item["id"], item["name"], item["price_cents"]),
            )
            self._recalculate(order_id)

    def change_quantity(self, order_item_id: int, delta: int):
        line = self.conn.execute(
            "SELECT * FROM order_items WHERE id = ?", (order_item_id,)
        ).fetchone()
        if line is None:
            raise OrderError("That item is no longer on the order.")
        order_id = line["order_id"]
        self._require_editable(order_id)
        if delta > 0 and self.item_count(order_id) + delta > config.MAX_ITEMS_PER_ORDER:
            raise OrderError(
                f"An order can have at most {config.MAX_ITEMS_PER_ORDER} items."
            )
        new_qty = line["quantity"] + delta
        with self.conn:
            if new_qty <= 0:
                self.conn.execute("DELETE FROM order_items WHERE id = ?", (order_item_id,))
            else:
                self.conn.execute(
                    "UPDATE order_items SET quantity = ? WHERE id = ?", (new_qty, order_item_id)
                )
            self._recalculate(order_id)

    def remove_line(self, order_item_id: int):
        line = self.conn.execute(
            "SELECT * FROM order_items WHERE id = ?", (order_item_id,)
        ).fetchone()
        if line is not None:
            self.change_quantity(order_item_id, -line["quantity"])

    def set_adjustments(self, order_id: int, discount: bool, surcharge: bool):
        self._require_editable(order_id)
        with self.conn:
            self.conn.execute(
                "UPDATE orders SET discount_applied = ?, surcharge_applied = ? WHERE id = ?",
                (int(discount), int(surcharge), order_id),
            )
            self._recalculate(order_id)

    def set_customer_name(self, order_id: int, name: str):
        self._require_editable(order_id)
        with self.conn:
            self.conn.execute(
                "UPDATE orders SET customer_name = ? WHERE id = ?", (name.strip(), order_id)
            )

    def send_to_kitchen(self, order_id: int):
        self._require_editable(order_id)
        if self.item_count(order_id) == 0:
            raise OrderError("Add at least one item before sending to the kitchen.")
        with self.conn:
            self.conn.execute(
                "UPDATE orders SET status = 'sent', sent_at = ? WHERE id = ?", (now(), order_id)
            )

    def complete(self, order_id: int):
        row = self._require_editable(order_id)
        if self.item_count(order_id) == 0:
            raise OrderError("Add at least one item before completing the order.")
        if row["slot"].startswith("TK") and not row["customer_name"]:
            raise OrderError("Takeaway orders need a customer name.")
        with self.conn:
            self.conn.execute(
                "UPDATE orders SET status = 'completed', closed_at = ? WHERE id = ?",
                (now(), order_id),
            )

    def void(self, order_id: int):
        self._require_editable(order_id)
        with self.conn:
            if self.item_count(order_id) == 0:
                # Nothing was ordered, so leave no trace in the reports.
                self.conn.execute("DELETE FROM orders WHERE id = ?", (order_id,))
            else:
                self.conn.execute(
                    "UPDATE orders SET status = 'void', closed_at = ? WHERE id = ?",
                    (now(), order_id),
                )

    # ---------- reports ----------

    def closed_orders_on(self, day: date, name_search: str = ""):
        """Completed and voided orders closed on the given local date."""
        sql = """SELECT * FROM orders
                 WHERE status IN ('completed', 'void') AND substr(closed_at, 1, 10) = ?"""
        params = [day.isoformat()]
        if name_search.strip():
            sql += " AND customer_name LIKE ? COLLATE NOCASE"
            params.append(f"%{name_search.strip()}%")
        return self.conn.execute(sql + " ORDER BY closed_at", params).fetchall()

    def daily_summary(self, day: date) -> dict:
        row = self.conn.execute(
            """SELECT
                 COALESCE(SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END), 0)               AS completed,
                 COALESCE(SUM(CASE WHEN status = 'void' THEN 1 ELSE 0 END), 0)                    AS voided,
                 COALESCE(SUM(CASE WHEN status = 'completed' THEN total_cents ELSE 0 END), 0)     AS revenue,
                 COALESCE(SUM(CASE WHEN status = 'completed' THEN discount_cents ELSE 0 END), 0)  AS discounts,
                 COALESCE(SUM(CASE WHEN status = 'completed' THEN surcharge_cents ELSE 0 END), 0) AS surcharges
               FROM orders WHERE substr(closed_at, 1, 10) = ?""",
            (day.isoformat(),),
        ).fetchone()
        return dict(row)
