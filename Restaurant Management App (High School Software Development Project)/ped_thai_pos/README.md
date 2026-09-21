# Ped Thai Cuisine POS

A desktop ordering system for Ped Thai Cuisine: tables, takeaway, the menu, and daily reports.

## Run it

Requires Python 3.10+ with Tkinter (included with the python.org installers for Windows and macOS; on Ubuntu/Debian run `sudo apt install python3-tk`). There are no other dependencies.

```
python run.py
```

The first launch asks you to create the admin account. There is no default password. Data is stored in `data/pos.db`. To keep it somewhere else, set the `PEDTHAI_DB` environment variable to a file path.

**Back up `data/pos.db`.** It holds every order. Copy it somewhere safe at the end of each day.

## Using it

- **Main screen:** tap a table or takeaway slot. White means available, green means an order is in progress, and yellow means it has been sent to the kitchen. Each busy slot shows its running total.
- **Ordering:** tap menu items to add them. Select a line and use − / + / Remove item to change it. Totals update live.
  - The discount and surcharge are tick boxes, so each applies at most once. The discount comes off the subtotal, and the surcharge is then added on the discounted amount.
  - Every change is saved immediately, so you can leave a table and come back, and nothing is lost if the app closes.
  - Complete order locks the order and frees the table. Takeaway orders need a customer name.
  - Void order cancels it. Voided orders stay in the reports but don't count as revenue.
- **Reports:** shows one day at a time: revenue, completed and voided orders, discounts and surcharges. You can search by customer name, click a column heading to sort, and double-click an order to see its items.

## Changing the menu, slots or rules

Edit `pos/config.py`:

- `SLOTS`: tables and takeaway slots
- `DISCOUNT_PERCENT`, `SURCHARGE_PERCENT`, `MAX_ITEMS_PER_ORDER`
- `DEFAULT_MENU`: used only when the database is first created. After that, the menu lives in the `menu_items` table. A menu editor screen is planned; until then, update prices with any SQLite tool. Past orders keep the price they were sold at.

## Tests

```
pip install pytest
python -m pytest
```

## What changed from the school version

| Old | Now |
|---|---|
| Pad-Se-Ew button crashed the app | Every menu item tested |
| Fried Rice charged $23 and was saved as "Pad-Se-Ew"; Kee Mao charged $21; Tempura charged $15 | Price shown = price charged, from one menu table |
| Discount/surcharge could be stacked any number of times | Each applies at most once, toggleable |
| Money stored as floats (`107.406`) | Integer cents, rounded half-up |
| Plain-text password in `Login_details.xml` | PBKDF2-hashed accounts, lockout after 5 failed attempts |
| 9 copy-pasted ordering files | One ordering screen for all slots |
| Pages launched each other via `subprocess(shell=True)` | One window, screens swap inside it |
| "Daily total" summed every order ever saved | Real per-day reports using the closing time |
| Delete / Send only showed a popup | Void and Send change the order's status |
| XML file rewritten on each save | SQLite with transactions |
| Crashed on macOS/Linux (`state("zoomed")`); buttons off-screen | Resizable layout, same on all platforms |

## Known limitations (next milestones)

- No kitchen display yet. "Send to kitchen" records the time and status only.
- No screen for managing staff accounts or editing the menu.
- No receipt printing or tax invoice. For card payments, use a separate terminal.
- Single computer only. Don't put `pos.db` on a shared network drive.
- The old `Customer.xml` test data is not imported.
