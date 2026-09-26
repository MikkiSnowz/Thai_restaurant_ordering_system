# Thai Restaurant Ordering System

A desktop point-of-sale app for Ped Thai Cuisine, built in Python with Tkinter and SQLite. It started as a high school software development project and has since been rebuilt.

## Features

- Tables and takeaway slots on one main screen, colour-coded by order status
- One ordering screen for every slot, with live totals
- One-time discount and surcharge (each applies at most once)
- Send to kitchen, complete and void order states
- Daily reports: revenue, completed and voided orders, search by customer, sortable columns, per-order detail
- Hashed staff logins with lockout after repeated failed attempts
- Orders saved instantly in SQLite, so nothing is lost if the app closes
- Money stored as integer cents, so totals are exact

## Quick start

Requires Python 3.10+ with Tkinter and no other dependencies.

```
cd "Restaurant Management App (High School Software Development Project)/ped_thai_pos"
python run.py
```

The first launch asks you to create the admin account. Data is stored in `data/pos.db`, or in the path set by the `PEDTHAI_DB` environment variable.

## Project layout

```
ped_thai_pos/
├── run.py          entry point
├── pos/
│   ├── config.py   slots, menu seed, discount/surcharge rules
│   ├── db.py       SQLite schema and order logic
│   ├── pricing.py  money and total calculations
│   ├── auth.py     password hashing
│   └── ui/         Tkinter screens (login, main menu, ordering, reports)
├── tests/          pytest suite
└── assets/         logo
```

## Tests

```
pip install pytest
python -m pytest
```

See [ped_thai_pos/README.md](Restaurant%20Management%20App%20%28High%20School%20Software%20Development%20Project%29/ped_thai_pos/README.md) for full usage, configuration, what changed from the school version, and known limitations.
