import os
import tkinter as tk
from tkinter import ttk, messagebox
import requests
from urllib.parse import urljoin

DEFAULT_API_BASE = "http://localhost:8080"


def _normalize_api_base(value: str | None) -> str:
    """Return a normalized API base URL with scheme and no trailing slash.

    Rules:
    - If value is None or empty/whitespace, fall back to DEFAULT_API_BASE.
    - If missing scheme, prepend "http://".
    - Strip trailing slash.
    """
    if not value or not value.strip():
        base = DEFAULT_API_BASE
    else:
        base = value.strip()
    if not (base.startswith("http://") or base.startswith("https://")):
        base = "http://" + base
    return base.rstrip('/')


API_BASE = _normalize_api_base(os.environ.get("API_BASE"))


class SchedulerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("AI-Sanatorium Scheduler")
        self.geometry("500x300")

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        frame = ttk.Frame(self, padding=16)
        frame.grid(row=0, column=0, sticky="nsew")
        frame.columnconfigure(0, weight=1)

        title = ttk.Label(frame, text="AI-Sanatorium Scheduler", font=("Arial", 16, "bold"))
        title.grid(row=0, column=0, pady=(0, 16))

        btn_health = ttk.Button(frame, text="Health Check", command=self.check_health)
        btn_health.grid(row=1, column=0, sticky="ew", pady=6)

        btn_run = ttk.Button(frame, text="Run Scheduler", command=self.run_scheduler)
        btn_run.grid(row=2, column=0, sticky="ew", pady=6)

        self.output = tk.Text(frame, height=10)
        self.output.grid(row=3, column=0, sticky="nsew", pady=8)
        frame.rowconfigure(3, weight=1)

    def check_health(self):
        try:
            health_url = urljoin(API_BASE + "/", "health")
            r = requests.get(health_url, timeout=5)
            r.raise_for_status()
            self.output.insert("end", f"Health: {r.json()}\n")
        except Exception as e:
            messagebox.showerror("Error", f"Health check failed: {e}")

    def run_scheduler(self):
        try:
            schedule_url = urljoin(API_BASE + "/", "schedule/run")
            r = requests.post(schedule_url, json=[], timeout=20)
            r.raise_for_status()
            self.output.insert("end", f"Schedule: {r.json()}\n")
        except Exception as e:
            messagebox.showerror("Error", f"Run scheduler failed: {e}")


if __name__ == "__main__":
    app = SchedulerApp()
    app.mainloop()
