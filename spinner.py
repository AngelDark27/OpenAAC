import tkinter as tk

class Spinner:
    def __init__(self, master, text="Loading", size=20, y_position=50):
        self.master = master
        self.size = size
        self.y_position = y_position
        self.text = text
        self.running = False
        self.frames = ["◐", "◓", "◑", "◒"]
        self.idx = 0

        self.label = tk.Label(master, text="", font=("Arial", self.size))
        self.label.place(relx=0.5, y=self.y_position, anchor="n")
        self.label.place_forget()


    def start(self):
        if self.running:
            return

        self.running = True
        self.idx = 0
        self.label.place(relx=0.5, y=self.y_position, anchor="n")
        self._animate()


    def _animate(self):
        if not self.running:
            return

        self.label.config(text=f"{self.frames[self.idx]} {self.text}...")
        self.idx = (self.idx + 1) % len(self.frames)
        self.master.after(150, self._animate)


    def stop(self):
        self.running = False
        self.label.place_forget()