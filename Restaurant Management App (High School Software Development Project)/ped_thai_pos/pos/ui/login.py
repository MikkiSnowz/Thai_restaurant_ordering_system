import time
import tkinter as tk
from tkinter import ttk

from .. import config
from ..db import OrderError
from . import theme


class _CenteredForm(ttk.Frame):
    """Shared layout: logo, title, then a white card holding the form."""

    def __init__(self, parent, app, title, subtitle):
        super().__init__(parent)
        self.app = app
        box = ttk.Frame(self)
        box.place(relx=0.5, rely=0.5, anchor="center")
        if app.logo:
            ttk.Label(box, image=app.logo).pack(pady=(0, 8))
        ttk.Label(box, text=title, style="Title.TLabel").pack()
        ttk.Label(box, text=subtitle, style="Muted.TLabel").pack(pady=(2, 16))
        self.card = ttk.Frame(box, style="Panel.TFrame", padding=24)
        self.card.pack()
        self.error = ttk.Label(self.card, text="", style="PanelError.TLabel", wraplength=320)

    def field(self, label, show=None):
        ttk.Label(self.card, text=label, style="Panel.TLabel").pack(anchor="w")
        var = tk.StringVar()
        entry = ttk.Entry(self.card, textvariable=var, width=32, font=theme.F_BODY, show=show or "")
        entry.pack(fill="x", pady=(2, 12))
        return var, entry

    def show_error(self, message):
        self.error.configure(text=message)


class SetupScreen(_CenteredForm):
    """Shown only when no accounts exist, so there is never a default password."""

    def __init__(self, parent, app):
        super().__init__(parent, app, f"{config.APP_NAME}",
                         "Create the admin account to get started")
        self.username, first = self.field("Username")
        self.password, _ = self.field("Password (at least 8 characters)", show="•")
        self.confirm, last = self.field("Confirm password", show="•")
        self.error.pack(fill="x", pady=(0, 8))
        ttk.Button(self.card, text="Create account", style="Primary.TButton",
                   command=self.submit).pack(fill="x")
        last.bind("<Return>", lambda e: self.submit())
        first.focus_set()

    def submit(self):
        if self.password.get() != self.confirm.get():
            return self.show_error("The passwords don't match.")
        try:
            self.app.db.create_user(self.username.get(), self.password.get(), role="admin")
        except OrderError as e:
            return self.show_error(str(e))
        self.app.login_as(self.app.db.authenticate(self.username.get(), self.password.get()))


class LoginScreen(_CenteredForm):
    failed = 0            # class-level so the count survives returning to this screen
    locked_until = 0.0

    def __init__(self, parent, app):
        super().__init__(parent, app, f"{config.APP_NAME}", "Sign in to start service")
        self.username, user_entry = self.field("Username")
        self.password, self.pw_entry = self.field("Password", show="•")
        self.show_pw = tk.BooleanVar()
        ttk.Checkbutton(self.card, text="Show password", variable=self.show_pw,
                        command=self.toggle_password).pack(anchor="w", pady=(0, 12))
        self.error.pack(fill="x", pady=(0, 8))
        self.button = ttk.Button(self.card, text="Sign in", style="Primary.TButton", command=self.submit)
        self.button.pack(fill="x")
        for w in (user_entry, self.pw_entry):
            w.bind("<Return>", lambda e: self.submit())
        user_entry.focus_set()
        self.tick_lockout()

    def toggle_password(self):
        self.pw_entry.configure(show="" if self.show_pw.get() else "•")

    def tick_lockout(self):
        remaining = int(LoginScreen.locked_until - time.monotonic() + 0.999)
        if remaining > 0:
            self.button.state(["disabled"])
            self.show_error(f"Too many failed attempts. Try again in {remaining} s.")
            self.after(500, self.tick_lockout)
        elif self.button.instate(["disabled"]):
            self.button.state(["!disabled"])
            self.show_error("")

    def submit(self):
        if time.monotonic() < LoginScreen.locked_until:
            return
        user, pw = self.username.get(), self.password.get()
        if not user or not pw:
            return self.show_error("Enter your username and password.")
        row = self.app.db.authenticate(user, pw)
        if row is None:
            LoginScreen.failed += 1
            self.password.set("")
            if LoginScreen.failed >= config.MAX_FAILED_LOGINS:
                LoginScreen.failed = 0
                LoginScreen.locked_until = time.monotonic() + config.LOCKOUT_SECONDS
                return self.tick_lockout()
            return self.show_error("Username or password is incorrect.")
        LoginScreen.failed = 0
        self.app.login_as(row)
