"""Business settings for Ped Thai Cuisine POS.

Change values here instead of hunting through UI code.
"""
import os
from pathlib import Path

APP_NAME = "Ped Thai Cuisine"

BASE_DIR = Path(__file__).resolve().parent.parent
ASSETS_DIR = BASE_DIR / "assets"
DB_PATH = Path(os.environ.get("PEDTHAI_DB", BASE_DIR / "data" / "pos.db"))

# Order slots shown on the main screen: (slot id, button label)
SLOTS = [(f"T{i}", f"Table {i}") for i in range(1, 7)] + [
    (f"TK{i}", f"Takeaway {i}") for i in range(1, 4)
]

# Pricing rules (whole-number percentages)
DISCOUNT_PERCENT = 10
SURCHARGE_PERCENT = 2

# Maximum total quantity of items on a single order (was 15 in the original app)
MAX_ITEMS_PER_ORDER = 15

# Login protection
MAX_FAILED_LOGINS = 5
LOCKOUT_SECONDS = 30

# Seed menu used the first time the database is created: (name, price in cents, category)
DEFAULT_MENU = [
    ("Gang Panang", 2100, "Curry"),
    ("Gang Massaman", 2700, "Curry"),
    ("Green Curry", 2300, "Curry"),
    ("Pad Thai", 2300, "Noodles & rice"),
    ("Pad-Se-Ew", 2000, "Noodles & rice"),
    ("Pad-Kee-Mao", 2400, "Noodles & rice"),
    ("Thai Fried Rice", 2000, "Noodles & rice"),
    ("Pad-Gapow", 2100, "Stir-fry"),
    ("Tom-Yum Soup", 1800, "Soup"),
    ("Kaitao", 1500, "Sides"),
    ("Tempura Vegetables", 2000, "Sides"),
    ("Coca-Cola", 400, "Drinks"),
]
