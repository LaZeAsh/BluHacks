import tkinter as tk
from tkinter import ttk
import cv2
from PIL import Image, ImageTk
import threading


class VideoRecorderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("BluHacks Training Dashboard")
        self.root.geometry("960x760")
        self.root.configure(bg="#0F172A")

        self.button_frame = ttk.Frame(self.root, style="My.TFrame", padding=(10, 0))
        self.button_frame.pack(side=tk.LEFT, padx=10, pady=10)

        self.pushups_button = ttk.Button(
            self.button_frame, text="Pushups", command=lambda: self.switch_exercise("Pushups")
        )
        self.pushups_button.pack(fill=tk.X, padx=10, pady=(5, 2))

        self.squats_button = ttk.Button(
            self.button_frame, text="Squats", command=lambda: self.switch_exercise("Squats")
        )
        self.squats_button.pack(fill=tk.X, padx=10, pady=2)

        self.situps_button = ttk.Button(
            self.button_frame, text="Situps", command=lambda: self.switch_exercise("Situps")
        )
        self.situps_button.pack(fill=tk.X, padx=10, pady=(2, 5))

        self.exercise_label = tk.Label(
            self.root,
            text="Exercise: None",
            font=("Helvetica", 24, "bold"),
            bg="#0F172A",
            fg="#38BDF8",
        )
        self.exercise_label.pack(pady=(30, 10))

        self.counter_label = tk.Label(
            self.root,
            text="Reps completed: 0",
            font=("Helvetica", 18),
            bg="#0F172A",
            fg="#E2E8F0",
        )
        self.counter_label.pack()

        self.video_label = tk.Label(self.root, bg="#0F172A")
        self.video_label.pack()

        self.start_button = ttk.Button(
            self.root, text="Start Recording", command=self.start_recording, style="My.TButton"
        )
        self.start_button.pack(pady=(20, 5))

        self.stop_button = ttk.Button(
            self.root,
            text="Stop Recording",
            command=self.stop_recording,
            state=tk.DISABLED,
            style="MyStop.TButton",
        )
        self.stop_button.pack()

        self.video_capture = cv2.VideoCapture(0)
        self.recording = False
        self.out = None
        self.recording_thread = None

        self.current_exercise = None
        self.counter = 0

        self.update_video()

    def update_video(self):
        ret, frame = self.video_capture.read()
        if ret:
            frame = cv2.flip(frame, 1)
            self.frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(self.frame))
            self.video_label.config(image=self.photo)
        self.root.after(10, self.update_video)

    def start_recording(self):
        self.recording = True
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.recording_thread = threading.Thread(target=self.record_video)
        self.recording_thread.start()

    def stop_recording(self):
        self.recording = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        if self.recording_thread is not None:
            self.recording_thread.join()
        if self.out is not None:
            self.out.release()

    def record_video(self):
        fourcc = cv2.VideoWriter_fourcc(*"MJPG")
        frame_width = int(self.video_capture.get(3))
        frame_height = int(self.video_capture.get(4))
        filename = f"{self.current_exercise}_output.avi"
        self.out = cv2.VideoWriter(filename, fourcc, 20, (frame_width, frame_height))

        while self.recording:
            ret, frame = self.video_capture.read()
            if ret:
                self.out.write(frame)
            else:
                break

    def switch_exercise(self, exercise):
        self.current_exercise = exercise
        self.exercise_label.config(text=f"Exercise: {exercise}")
        self.counter = 0
        self.update_counter()

    def update_counter(self):
        self.counter_label.config(text=f"Reps completed: {self.counter}")


root = tk.Tk()
root.title("BluHacks Training Dashboard")

style = ttk.Style(root)
style.theme_use("clam")

style.configure("My.TFrame", background="#191414", borderwidth=0, relief=tk.FLAT)
style.configure(
    "My.TButton",
    background="#1DB954",
    foreground="white",
    borderwidth=0,
    relief=tk.FLAT,
    font=("Spotify", 14),
)
style.map("My.TButton", background=[("active", "#1ed760")])

style.configure(
    "MyStop.TButton",
    background="#FF0000",
    foreground="white",
    borderwidth=0,
    relief=tk.FLAT,
    font=("Spotify", 14),
)
style.map("MyStop.TButton", background=[("active", "#FF3030")])

app = VideoRecorderApp(root)
root.mainloop()
