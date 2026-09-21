"""Colours, fonts and ttk styles shared by every screen."""
from tkinter import ttk

BG = "#EEF0EA"          # rice-paper grey-green background
PANEL = "#FFFFFF"
INK = "#1D2320"
MUTED = "#5C6660"
LINE = "#D5D9D1"
BASIL = "#2F5D3A"       # primary actions
BASIL_DARK = "#224429"
TURMERIC = "#E3A52B"    # "sent to kitchen" / attention
TURMERIC_DARK = "#C68B17"
CHILI = "#B3261E"       # destructive actions
CHILI_DARK = "#8E1D17"
BASIL_TINT = "#DCE8DE"
TURMERIC_TINT = "#FBEBC8"

FAMILY = "Helvetica"
F_BODY = (FAMILY, 13)
F_SMALL = (FAMILY, 11)
F_LABEL = (FAMILY, 13, "bold")
F_TITLE = (FAMILY, 22, "bold")
F_BIG = (FAMILY, 26, "bold")
F_TILE = (FAMILY, 14, "bold")


def apply(root):
    root.configure(bg=BG)
    s = ttk.Style(root)
    s.theme_use("clam")  # the native macOS theme ignores button colours

    s.configure(".", background=BG, foreground=INK, font=F_BODY)
    s.configure("TFrame", background=BG)
    s.configure("Panel.TFrame", background=PANEL)
    s.configure("Header.TFrame", background=BASIL_DARK)

    s.configure("TLabel", background=BG, foreground=INK)
    s.configure("Panel.TLabel", background=PANEL)
    s.configure("Muted.TLabel", foreground=MUTED, font=F_SMALL)
    s.configure("PanelMuted.TLabel", background=PANEL, foreground=MUTED, font=F_SMALL)
    s.configure("Title.TLabel", font=F_TITLE)
    s.configure("PanelTitle.TLabel", background=PANEL, font=F_LABEL)
    s.configure("Header.TLabel", background=BASIL_DARK, foreground="white", font=F_TITLE)
    s.configure("HeaderMuted.TLabel", background=BASIL_DARK, foreground="#C9D8CC", font=F_BODY)
    s.configure("Total.TLabel", background=PANEL, font=F_BIG)
    s.configure("Error.TLabel", foreground=CHILI, font=F_LABEL)
    s.configure("PanelError.TLabel", background=PANEL, foreground=CHILI, font=F_LABEL)
    s.configure("Stat.TLabel", background=PANEL, font=(FAMILY, 20, "bold"))

    s.configure("TCheckbutton", background=PANEL, font=F_BODY)
    s.map("TCheckbutton", background=[("active", PANEL)])
    s.configure("TEntry", padding=6)

    def button(name, bg, active, fg="white", font=F_LABEL, pad=(14, 10)):
        s.configure(name, background=bg, foreground=fg, font=font, padding=pad,
                    borderwidth=0, focusthickness=2, focuscolor=INK)
        s.map(name,
              background=[("disabled", LINE), ("pressed", active), ("active", active)],
              foreground=[("disabled", MUTED)])

    button("TButton", "#E2E6DE", "#D0D6CB", fg=INK)
    button("Primary.TButton", BASIL, BASIL_DARK)
    button("Accent.TButton", TURMERIC, TURMERIC_DARK, fg=INK)
    button("Danger.TButton", CHILI, CHILI_DARK)
    button("Header.TButton", BASIL, "#3B7349", pad=(12, 6))
    button("Qty.TButton", "#E2E6DE", "#D0D6CB", fg=INK, font=(FAMILY, 16, "bold"), pad=(12, 4))
    button("Tile.TButton", PANEL, BASIL_TINT, fg=INK, font=F_TILE, pad=(10, 14))
    for name in ("Tile.TButton", "SlotFree.TButton", "SlotOpen.TButton", "SlotSent.TButton"):
        s.configure(name, justify="center")
    # Main-screen slot tiles, one style per state
    button("SlotFree.TButton", PANEL, BASIL_TINT, fg=INK, font=F_TILE, pad=(10, 24))
    button("SlotOpen.TButton", BASIL_TINT, "#C6DAC9", fg=INK, font=F_TILE, pad=(10, 24))
    button("SlotSent.TButton", TURMERIC_TINT, "#F5DDA4", fg=INK, font=F_TILE, pad=(10, 24))

    s.configure("Treeview", background=PANEL, fieldbackground=PANEL, rowheight=30, font=F_BODY)
    s.configure("Treeview.Heading", background="#E2E6DE", font=F_LABEL, relief="flat")
    s.map("Treeview", background=[("selected", BASIL_TINT)], foreground=[("selected", INK)])
