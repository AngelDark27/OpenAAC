import tkinter as tk

class Spinner:
    def __init__(self, master, text="Loading", size=20):
        self.master = master
        self.size = size
        self.text = text
        self.running = False
        self.label = None
        self.frames = ["◐", "◓", "◑", "◒"]
        self.idx = 0

    def start(self):
        if self.label is None:
            self.label = tk.Label(self.master, text="", font=("Arial", self.size))
            self.label.pack(pady=5)
        self.running = True
        self._animate()

    def _animate(self):
        if self.running:
            self.label.config(text=f"{self.frames[self.idx]} {self.text}...")
            self.idx = (self.idx + 1) % len(self.frames)
            self.master.after(200, self._animate)

    def stop(self):
        self.running = False
        if self.label:
            self.label.pack_forget()