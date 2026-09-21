"""One window for the whole app. Screens swap inside it instead of
launching separate scripts with subprocess."""
import tkinter as tk
from tkinter import ttk

from .. import config
from ..db import Database
from . import theme


class App:
    def __init__(self, db: Database):
        self.db = db
        self.user = None
        self.root = tk.Tk()
        self.root.title(f"{config.APP_NAME} POS")
        self.root.geometry("1280x800")
        self.root.minsize(1024, 700)
        theme.apply(self.root)
        self.root.protocol("WM_DELETE_WINDOW", self.quit)
        self.screen = None
        self.logo = None
        logo_path = config.ASSETS_DIR / "Logo.png"
        if logo_path.exists():
            try:
                self.logo = tk.PhotoImage(file=str(logo_path), master=self.root)
            except tk.TclError:
                self.logo = None  # a missing or unreadable logo shouldn't stop the till

    def show(self, screen_cls, **kwargs):
        if self.screen is not None:
            self.screen.destroy()
        self.screen = screen_cls(self.root, self, **kwargs)
        self.screen.pack(fill="both", expand=True)

    def start(self):
        from .login import LoginScreen, SetupScreen
        self.show(SetupScreen if self.db.user_count() == 0 else LoginScreen)

    def login_as(self, user):
        from .main_menu import MainMenu
        self.user = user
        self.show(MainMenu)

    def logout(self):
        from .login import LoginScreen
        self.user = None
        self.show(LoginScreen)

    def quit(self):
        self.db.close()
        self.root.destroy()

    def run(self):
        self.start()
        self.root.mainloop()


def header(parent, app, title, back=None, back_label="Back"):
    """Dark bar across the top of a screen with an optional back button."""
    bar = ttk.Frame(parent, style="Header.TFrame", padding=(20, 12))
    bar.pack(fill="x")
    if back:
        ttk.Button(bar, text=back_label, style="Header.TButton", command=back).pack(side="left", padx=(0, 16))
    ttk.Label(bar, text=title, style="Header.TLabel").pack(side="left")
    if app.user is not None:
        ttk.Label(bar, text=f"Signed in as {app.user['username']}", style="HeaderMuted.TLabel").pack(side="right")
    return bar
