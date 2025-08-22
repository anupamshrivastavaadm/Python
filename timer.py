import tkinter as tk
import winsound  # works on Windows for beep sound
import threading

class TimerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Custom Tkinter Timer ⏱️")

        # State variables
        self.running = False
        self.time_left = 0
        self.beeping = False

        # Input fields
        input_frame = tk.Frame(root)
        input_frame.pack(pady=10)

        tk.Label(input_frame, text="Minutes:").pack(side="left")
        self.min_entry = tk.Entry(input_frame, width=5)
        self.min_entry.insert(0, "1")  # default = 1 min
        self.min_entry.pack(side="left", padx=5)

        tk.Label(input_frame, text="Seconds:").pack(side="left")
        self.sec_entry = tk.Entry(input_frame, width=5)
        self.sec_entry.insert(0, "0")
        self.sec_entry.pack(side="left", padx=5)

        # Timer display
        self.label = tk.Label(root, text="00:00", font=("Arial", 40))
        self.label.pack(pady=20)

        # Buttons
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=10)

        self.start_btn = tk.Button(btn_frame, text="Start", command=self.start_timer, width=10)
        self.start_btn.pack(side="left", padx=5)

        self.pause_btn = tk.Button(btn_frame, text="Pause", command=self.pause_timer, width=10)
        self.pause_btn.pack(side="left", padx=5)

        self.reset_btn = tk.Button(btn_frame, text="Reset", command=self.reset_timer, width=10)
        self.reset_btn.pack(side="left", padx=5)

    def format_time(self, seconds):
        mins, secs = divmod(seconds, 60)
        return f"{mins:02}:{secs:02}"

    def update_timer(self):
        if self.running and self.time_left > 0:
            self.time_left -= 1
            self.label.config(text=self.format_time(self.time_left))
            self.root.after(1000, self.update_timer)
        elif self.time_left == 0 and self.running:
            self.label.config(text="Time's Up!")
            self.running = False
            self.start_beeping()

    def start_timer(self):
        if not self.running:
            try:
                mins = int(self.min_entry.get())
                secs = int(self.sec_entry.get())
                self.time_left = mins * 60 + secs
            except ValueError:
                self.time_left = 60  # fallback default
            self.label.config(text=self.format_time(self.time_left))
            self.running = True
            self.update_timer()

    def pause_timer(self):
        self.running = False
        self.stop_beeping()

    def reset_timer(self):
        self.running = False
        self.stop_beeping()
        self.label.config(text="00:00")

    def start_beeping(self):
        self.beeping = True
        threading.Thread(target=self._beep_loop, daemon=True).start()

    def _beep_loop(self):
        while self.beeping:
            winsound.Beep(1000, 500)  # frequency=1000Hz, duration=500ms
            self.root.after(500)      # small pause

    def stop_beeping(self):
        self.beeping = False


if __name__ == "__main__":
    root = tk.Tk()
    app = TimerApp(root)
    root.mainloop()
