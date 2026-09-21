from datetime import date

import pytest

from pos import auth, config
from pos.db import Database, OrderError
from pos.pricing import calculate_totals, format_money, percent_of


# ---------- pricing ----------

def test_percent_rounds_half_up():
    assert percent_of(2150, 10) == 215
    assert percent_of(125, 2) == 3        # 2.5 cents -> 3
    assert percent_of(0, 10) == 0


def test_totals_discount_then_surcharge_once():
    lines = [(2100, 1), (2700, 1), (2300, 2)]  # 94.00
    t = calculate_totals(lines, True, True, 10, 2)
    assert t.subtotal == 9400
    assert t.discount == 940                  # 10% of 94.00
    assert t.surcharge == 169                 # 2% of 84.60 = 1.692 -> 1.69
    assert t.total == 9400 - 940 + 169


def test_totals_without_adjustments():
    t = calculate_totals([(400, 3)], False, False, 10, 2)
    assert (t.subtotal, t.discount, t.surcharge, t.total) == (1200, 0, 0, 1200)


def test_format_money():
    assert format_money(2100) == "$21.00"
    assert format_money(123456) == "$1,234.56"
    assert format_money(5) == "$0.05"


# ---------- auth ----------

def test_password_hash_roundtrip():
    stored = auth.hash_password("correct horse")
    assert "correct horse" not in stored
    assert auth.verify_password("correct horse", stored)
    assert not auth.verify_password("wrong", stored)
    assert not auth.verify_password("x", "garbage")


# ---------- database ----------

@pytest.fixture
def db():
    d = Database(":memory:")
    yield d
    d.close()


def menu_id(db, name):
    return next(m["id"] for m in db.menu() if m["name"] == name)


def test_menu_prices_match_what_is_shown(db):
    # Regression: the old app charged $23 for Fried Rice, $21 for Kee Mao, $15 for Tempura.
    prices = {m["name"]: m["price_cents"] for m in db.menu()}
    assert prices["Thai Fried Rice"] == 2000
    assert prices["Pad-Kee-Mao"] == 2400
    assert prices["Tempura Vegetables"] == 2000
    assert prices["Pad-Se-Ew"] == 2000


def test_every_menu_item_can_be_ordered(db):
    # Regression: Pad-Se-Ew crashed the old app.
    oid = db.get_or_create_active_order("T1", None)
    for m in db.menu():
        db.add_item(oid, m["id"])
    expected = sum(m["price_cents"] for m in db.menu())
    assert db.order(oid)["total_cents"] == expected


def test_same_item_increments_quantity(db):
    oid = db.get_or_create_active_order("T1", None)
    pad_thai = menu_id(db, "Pad Thai")
    db.add_item(oid, pad_thai)
    db.add_item(oid, pad_thai)
    items = db.items(oid)
    assert len(items) == 1 and items[0]["quantity"] == 2
    assert db.order(oid)["total_cents"] == 4600


def test_quantity_down_to_zero_removes_line(db):
    oid = db.get_or_create_active_order("T1", None)
    db.add_item(oid, menu_id(db, "Coca-Cola"))
    line = db.items(oid)[0]
    db.change_quantity(line["id"], -1)
    assert db.items(oid) == []
    assert db.order(oid)["total_cents"] == 0


def test_item_limit(db):
    oid = db.get_or_create_active_order("T1", None)
    coke = menu_id(db, "Coca-Cola")
    for _ in range(config.MAX_ITEMS_PER_ORDER):
        db.add_item(oid, coke)
    with pytest.raises(OrderError):
        db.add_item(oid, coke)


def test_adjustments_toggle_not_stack(db):
    oid = db.get_or_create_active_order("T1", None)
    db.add_item(oid, menu_id(db, "Gang Massaman"))   # 27.00
    db.set_adjustments(oid, True, True)
    db.set_adjustments(oid, True, True)              # applying again changes nothing
    o = db.order(oid)
    assert o["discount_cents"] == 270
    assert o["surcharge_cents"] == 49                # 2% of 24.30 = 0.486 -> 0.49
    assert o["total_cents"] == 2700 - 270 + 49
    db.set_adjustments(oid, False, False)
    assert db.order(oid)["total_cents"] == 2700


def test_price_change_does_not_rewrite_history(db):
    oid = db.get_or_create_active_order("T1", None)
    pid = menu_id(db, "Pad Thai")
    db.add_item(oid, pid)
    db.complete(oid)
    with db.conn:
        db.conn.execute("UPDATE menu_items SET price_cents = 9999 WHERE id = ?", (pid,))
    assert db.order(oid)["total_cents"] == 2300


def test_one_active_order_per_slot(db):
    a = db.get_or_create_active_order("T2", None)
    b = db.get_or_create_active_order("T2", None)
    assert a == b


def test_completed_order_is_locked(db):
    oid = db.get_or_create_active_order("T1", None)
    db.add_item(oid, menu_id(db, "Pad Thai"))
    db.complete(oid)
    with pytest.raises(OrderError):
        db.add_item(oid, menu_id(db, "Pad Thai"))
    # Slot is free for a new order afterwards
    assert db.get_or_create_active_order("T1", None) != oid


def test_cannot_complete_empty_order(db):
    oid = db.get_or_create_active_order("T1", None)
    with pytest.raises(OrderError):
        db.complete(oid)


def test_takeaway_needs_name(db):
    oid = db.get_or_create_active_order("TK1", None)
    db.add_item(oid, menu_id(db, "Pad Thai"))
    with pytest.raises(OrderError):
        db.complete(oid)
    db.set_customer_name(oid, "  Somchai  ")
    db.complete(oid)
    assert db.order(oid)["customer_name"] == "Somchai"


def test_send_to_kitchen_sets_status(db):
    oid = db.get_or_create_active_order("T1", None)
    with pytest.raises(OrderError):
        db.send_to_kitchen(oid)
    db.add_item(oid, menu_id(db, "Pad Thai"))
    db.send_to_kitchen(oid)
    o = db.order(oid)
    assert o["status"] == "sent" and o["sent_at"]
    db.add_item(oid, menu_id(db, "Coca-Cola"))       # still editable after sending


def test_void_empty_order_leaves_no_record(db):
    oid = db.get_or_create_active_order("T1", None)
    db.void(oid)
    assert db.order(oid) is None


def test_daily_summary_counts_only_completed(db):
    for slot, item, finish in [("T1", "Pad Thai", "complete"),
                               ("T2", "Gang Massaman", "complete"),
                               ("T3", "Coca-Cola", "void")]:
        oid = db.get_or_create_active_order(slot, None)
        db.add_item(oid, menu_id(db, item))
        getattr(db, finish)(oid)
    s = db.daily_summary(date.today())
    assert s["completed"] == 2 and s["voided"] == 1
    assert s["revenue"] == 2300 + 2700
    assert db.daily_summary(date(2000, 1, 1))["revenue"] == 0


def test_search_by_name(db):
    for slot, name in [("T1", "Nguyen"), ("T2", "Smith")]:
        oid = db.get_or_create_active_order(slot, None)
        db.add_item(oid, menu_id(db, "Pad Thai"))
        db.set_customer_name(oid, name)
        db.complete(oid)
    rows = db.closed_orders_on(date.today(), "ngu")
    assert [r["customer_name"] for r in rows] == ["Nguyen"]


def test_users(db):
    assert db.user_count() == 0
    db.create_user("Admin", "longenough1", "admin")
    assert db.authenticate("admin", "longenough1")["role"] == "admin"   # case-insensitive username
    assert db.authenticate("admin", "wrong-password") is None
    with pytest.raises(OrderError):
        db.create_user("ADMIN", "anotherpass1")
    with pytest.raises(OrderError):
        db.create_user("bob", "short")


def test_open_order_survives_restart(tmp_path):
    path = tmp_path / "pos.db"
    d = Database(path)
    oid = d.get_or_create_active_order("T4", None)
    d.add_item(oid, menu_id(d, "Pad Thai"))
    d.close()
    d = Database(path)          # simulate closing and reopening the app
    assert d.active_order("T4")["total_cents"] == 2300
    assert len(d.menu()) == len(config.DEFAULT_MENU)   # menu not seeded twice
    d.close()
