import tkinter as tk
from tkinter import messagebox, ttk
import secrets
import string
from pathlib import Path

RESET_SECONDS = 60
PASSWORD_CHARACTERS = string.ascii_letters + string.digits + "!@#$%&*_-+="


class PasswordGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Password Generator")
        self.root.geometry("560x500")
        self.root.minsize(520, 470)
        self.root.configure(bg="#0B1120")

        self.running = False
        self.timer_id = None
        self.seconds_left = RESET_SECONDS

        self._setup_style()
        self._build_ui()
        self.root.protocol("WM_DELETE_WINDOW", self.close)

        icon_path = Path(__file__).with_name("app_icon.ico")
        if icon_path.exists():
            try:
                self.root.iconbitmap(str(icon_path))
            except tk.TclError:
                pass

    def _setup_style(self):
        style = ttk.Style(self.root)
        style.theme_use("clam")
        style.configure("TFrame", background="#0B1120")
        style.configure("Card.TFrame", background="#111C2E")
        style.configure("TLabel", background="#0B1120", foreground="#E5EDF7", font=("Segoe UI", 10))
        style.configure("Muted.TLabel", background="#0B1120", foreground="#91A2B8", font=("Segoe UI", 9))
        style.configure("Card.TLabel", background="#111C2E", foreground="#E5EDF7", font=("Segoe UI", 10))
        style.configure("CardMuted.TLabel", background="#111C2E", foreground="#91A2B8", font=("Segoe UI", 9))
        style.configure("Title.TLabel", background="#0B1120", foreground="#F4F8FF", font=("Segoe UI", 22, "bold"))
        style.configure("Subtitle.TLabel", background="#0B1120", foreground="#91A2B8", font=("Segoe UI", 10))
        style.configure("TEntry", fieldbackground="#0B1526", foreground="#F4F8FF", insertcolor="#F4F8FF", bordercolor="#26364D", lightcolor="#26364D", darkcolor="#26364D", padding=10)
        style.configure("Password.TEntry", fieldbackground="#0B1526", foreground="#5EF0B1", insertcolor="#5EF0B1", bordercolor="#26364D", lightcolor="#26364D", darkcolor="#26364D", padding=13, font=("Consolas", 13))
        style.configure("TButton", font=("Segoe UI", 10, "bold"), padding=(12, 10), background="#26364D", foreground="#E5EDF7", borderwidth=0)
        style.map("TButton", background=[("active", "#344965"), ("disabled", "#1A2739")], foreground=[("disabled", "#65768D")])
        style.configure("Accent.TButton", background="#0EA5E9", foreground="#03111C")
        style.map("Accent.TButton", background=[("active", "#38BDF8"), ("disabled", "#1A2739")], foreground=[("disabled", "#65768D")])
        style.configure("Green.TButton", background="#10B981", foreground="#03150F")
        style.map("Green.TButton", background=[("active", "#34D399")])
        style.configure("Danger.TButton", background="#26364D", foreground="#FCA5A5")
        style.map("Danger.TButton", background=[("active", "#3B2635")])

    def _build_ui(self):
        outer = ttk.Frame(self.root, padding=(30, 25, 30, 22))
        outer.pack(fill="both", expand=True)

        ttk.Label(outer, text="SECURE TOOLS  /  PASSWORDS", style="Muted.TLabel").pack(anchor="w")
        ttk.Label(outer, text="Password Generator", style="Title.TLabel").pack(anchor="w", pady=(8, 3))
        ttk.Label(outer, text="Create a strong password, right on your device.", style="Subtitle.TLabel").pack(anchor="w")

        card = ttk.Frame(outer, style="Card.TFrame", padding=22)
        card.pack(fill="x", pady=(24, 16))

        ttk.Label(card, text="PASSWORD LENGTH", style="CardMuted.TLabel").pack(anchor="w")
        length_row = ttk.Frame(card, style="Card.TFrame")
        length_row.pack(fill="x", pady=(8, 20))
        self.length_entry = ttk.Entry(length_row, width=12, justify="center")
        self.length_entry.insert(0, "16")
        self.length_entry.pack(side="left")
        ttk.Label(length_row, text="Choose 8–128 characters", style="CardMuted.TLabel").pack(side="left", padx=12)

        ttk.Label(card, text="YOUR PASSWORD", style="CardMuted.TLabel").pack(anchor="w", pady=(0, 8))
        password_row = ttk.Frame(card, style="Card.TFrame")
        password_row.pack(fill="x")
        self.password_var = tk.StringVar()
        self.password_entry = ttk.Entry(password_row, textvariable=self.password_var, style="Password.TEntry", state="readonly")
        self.password_entry.pack(side="left", fill="x", expand=True)
        self.copy_button = ttk.Button(password_row, text="Copy", command=self.copy_password)
        self.copy_button.pack(side="left", padx=(10, 0), ipady=3)

        actions = ttk.Frame(outer)
        actions.pack(fill="x", pady=(2, 0))
        ttk.Button(actions, text="Generate password", style="Accent.TButton", command=self.generate_password).pack(side="left", fill="x", expand=True)
        self.start_button = ttk.Button(actions, text="Auto refresh", style="Green.TButton", command=self.start_auto_refresh)
        self.start_button.pack(side="left", fill="x", expand=True, padx=(10, 0))
        self.stop_button = ttk.Button(actions, text="Stop", style="Danger.TButton", command=self.stop_auto_refresh, state="disabled")
        self.stop_button.pack(side="left", fill="x", expand=True, padx=(10, 0))

        self.status_var = tk.StringVar(value="Ready — generate a password to get started.")
        ttk.Label(outer, textvariable=self.status_var, style="Muted.TLabel", wraplength=480).pack(anchor="w", pady=(20, 8))

        ttk.Separator(outer).pack(fill="x", pady=(5, 12))
        ttk.Label(
            outer,
            text="Generated locally on your computer. This app does not change your Windows or account login password. Copy and save passwords you want to keep before they refresh.",
            style="Muted.TLabel",
            wraplength=490,
            justify="left"
        ).pack(anchor="w")

    def _read_length(self):
        try:
            length = int(self.length_entry.get())
        except ValueError:
            messagebox.showerror("Invalid length", "Enter a whole number between 8 and 128.", parent=self.root)
            return None
        if not 8 <= length <= 128:
            messagebox.showerror("Invalid length", "Password length must be between 8 and 128.", parent=self.root)
            return None
        return length

    def generate_password(self):
        length = self._read_length()
        if length is None:
            return None
        password = "".join(secrets.choice(PASSWORD_CHARACTERS) for _ in range(length))
        self.password_var.set(password)
        if not self.running:
            self.status_var.set("Password generated. Copy it somewhere safe if you want to keep it.")
        return password

    def start_auto_refresh(self):
        if self.running:
            return
        if self.generate_password() is None:
            return
        self.running = True
        self.seconds_left = RESET_SECONDS
        self.start_button.configure(state="disabled")
        self.stop_button.configure(state="normal")
        self._tick()

    def _tick(self):
        if not self.running:
            return
        if self.seconds_left <= 0:
            if self.generate_password() is None:
                self.stop_auto_refresh()
                return
            self.seconds_left = RESET_SECONDS
        self.status_var.set(f"Automatic refresh is on · next password in {self.seconds_left} seconds")
        self.seconds_left -= 1
        self.timer_id = self.root.after(1000, self._tick)

    def stop_auto_refresh(self):
        self.running = False
        if self.timer_id is not None:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None
        self.start_button.configure(state="normal")
        self.stop_button.configure(state="disabled")
        self.status_var.set("Automatic refresh stopped.")

    def copy_password(self):
        password = self.password_var.get()
        if not password:
            self.status_var.set("Generate a password before copying.")
            return
        self.root.clipboard_clear()
        self.root.clipboard_append(password)
        self.root.update_idletasks()
        self.status_var.set("Password copied to the clipboard.")

    def close(self):
        self.stop_auto_refresh()
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    PasswordGeneratorApp(root)
    root.mainloop()
