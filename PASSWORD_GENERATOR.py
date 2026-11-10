import tkinter as tk
from tkinter import messagebox
import secrets
import string

RESET_SECONDS = 60
PASSWORD_CHARACTERS = string.ascii_letters + string.digits + "!@#$%&*_-+="
timer_id = None
running = False


def generate_password():
    try:
        length = int(length_entry.get())
    except ValueError:
        messagebox.showerror("Invalid length", "Enter a whole number.")
        return None

    if not 8 <= length <= 128:
        messagebox.showerror(
            "Invalid length",
            "Password length must be between 8 and 128."
        )
        return None

    password = "".join(secrets.choice(PASSWORD_CHARACTERS) for _ in range(length))
    password_var.set(password)
    return password


def schedule_tick(seconds):
    global timer_id

    timer_label.config(text=f"Next reset in: {seconds} seconds")
    if seconds == 0:
        if running and generate_password() is not None:
            schedule_tick(RESET_SECONDS)
        else:
            stop_app()
        return

    timer_id = app.after(1000, lambda: schedule_tick(seconds - 1))


def start_app():
    global running
    if running:
        return

    if generate_password() is None:
        return

    running = True
    start_button.config(state="disabled")
    schedule_tick(RESET_SECONDS)


def stop_app():
    global running, timer_id
    running = False

    if timer_id is not None:
        app.after_cancel(timer_id)
        timer_id = None

    start_button.config(state="normal")
    timer_label.config(text="Automatic reset stopped")


def copy_password():
    password = password_var.get()
    if not password:
        messagebox.showinfo("No password", "Generate a password first.")
        return

    app.clipboard_clear()
    app.clipboard_append(password)
    app.update()
    messagebox.showinfo("Copied", "Password copied to clipboard.")


app = tk.Tk()
app.title("Password Generator")
app.geometry("480x390")
app.resizable(False, False)
app.configure(bg="#101820")

# The Windows executable gets its icon from the PyInstaller --icon build option.
# When running the Python source directly, use the generated icon if available.
try:
    app.iconbitmap(default="app_icon.ico")
except tk.TclError:
    pass

tk.Label(
    app,
    text="PASSWORD GENERATOR",
    font=("Arial", 21, "bold"),
    bg="#101820",
    fg="#00D9FF"
).pack(pady=(24, 18))

tk.Label(
    app,
    text="Password length (8–128):",
    font=("Arial", 12),
    bg="#101820",
    fg="white"
).pack()

length_entry = tk.Entry(app, font=("Arial", 14), justify="center", width=12)
length_entry.insert(0, "16")
length_entry.pack(pady=8)

password_var = tk.StringVar()
password_display = tk.Entry(
    app,
    textvariable=password_var,
    font=("Consolas", 13),
    justify="center",
    state="readonly",
    readonlybackground="#202E3A",
    fg="#00FF99",
    width=38
)
password_display.pack(padx=20, pady=18, ipady=9)

timer_label = tk.Label(
    app,
    text="Press START to generate a password",
    font=("Arial", 13),
    bg="#101820",
    fg="#FFE066"
)
timer_label.pack(pady=8)

start_button = tk.Button(
    app,
    text="START AUTO RESET",
    command=start_app,
    bg="#00A86B",
    fg="white",
    font=("Arial", 11, "bold"),
    width=22
)
start_button.pack(pady=5)

tk.Button(
    app,
    text="COPY PASSWORD",
    command=copy_password,
    bg="#1677FF",
    fg="white",
    font=("Arial", 10, "bold"),
    width=22
).pack(pady=4)

tk.Button(
    app,
    text="STOP",
    command=stop_app,
    bg="#D62828",
    fg="white",
    font=("Arial", 10, "bold"),
    width=22
).pack(pady=4)

tk.Label(
    app,
    text="Refreshes the displayed password every 60 seconds.\n"
         "It does not change your Windows or device login password.",
    font=("Arial", 9),
    bg="#101820",
    fg="#AAB4BE",
    justify="center"
).pack(pady=(12, 0))

app.mainloop()
