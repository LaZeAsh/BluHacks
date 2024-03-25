import tkinter as tk
from tkinter import ttk
import cv2
from PIL import Image, ImageTk
import threading
import detector
import pygame
import time

class VideoRecorderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Video Recorder App")
        self.root.geometry("800x800")
        self.root.configure(bg="#191414")  # Set background color to Spotify's dark theme
        self.total_pushups = 0
        self.total_squats = 0
        self.total_situps = 0
        self.money = 5
        self.music_enabled = False
        self.inventory = []
        self.shop_items = ["small trophy", "5", "decent size trophy", "20", "biggg trophy", "50", "biggest.", "100"]
        self.toggle_music()

        # Create a frame for buttons on the left side
        self.button_frame = ttk.Frame(self.root, style="My.TFrame", padding=(10, 0))
        self.button_frame.pack(side=tk.LEFT, padx=10, pady=10)

        

        self.pushup_counter_label = tk.Label(self.button_frame, text="Total Pushups: 0", bg="#191414", fg="white")
        self.pushup_counter_label.pack(side=tk.TOP)

        # Add buttons for exercises
        self.pushups_button = ttk.Button(self.button_frame, text="Pushups", command=lambda: self.switch_exercise("Pushups"))
        self.pushups_button.pack(fill=tk.X, padx=10, pady=(5, 2))

        self.squats_counter_label = tk.Label(self.button_frame, text="Total Squats: 0", font=("Spotify", 16), bg="#191414", fg="white")
        self.squats_counter_label.pack(side=tk.TOP)

        self.squats_button = ttk.Button(self.button_frame, text="Squats", command=lambda: self.switch_exercise("Squats"))
        self.squats_button.pack(fill=tk.X, padx=10, pady=2)

        self.situps_counter_label = tk.Label(self.button_frame, text="Total Situps: 0", font=("Spotify", 16), bg="#191414", fg="white")
        self.situps_counter_label.pack(side=tk.TOP)

        self.situps_button = ttk.Button(self.button_frame, text="Situps", command=lambda: self.switch_exercise("Situps"))
        self.situps_button.pack(fill=tk.X, padx=10, pady=(2, 5))

        # Header and counter for exercise tracking
        self.exercise_label = tk.Label(self.root, text="Exercise: None", font=("Spotify", 20), bg="#191414", fg="#1DB954")
        self.exercise_label.pack(pady=(30, 10))

        self.counter_label = tk.Label(self.root, text="Count: 0", font=("Spotify", 16), bg="#191414", fg="white")
        self.counter_label.pack()

        self.money_counter_label = tk.Label(self.root, text="Money $DUCK: 5", font=("Spotify", 16), bg="#191414", fg="white")
        self.money_counter_label.pack()

        

        # Create a label for video display
        self.video_label = tk.Label(self.root, bg="#191414")
        self.video_label.pack()

        # Create buttons for video recording
        self.start_button = ttk.Button(self.root, text="Start Recording", command=self.start_recording, style="My.TButton")
        self.start_button.pack(pady=(20, 5))

        self.stop_button = ttk.Button(self.root, text="Stop Recording", command=self.stop_recording, state=tk.DISABLED, style="MyStop.TButton")
        self.stop_button.pack()

        #create button for music
        self.music_button = ttk.Button(self.root, text="Toggle Music", command=self.toggle_music)
        self.music_button.pack(side=tk.LEFT)

        self.shop_button = ttk.Button(self.root, text="Shop", command=self.shop)
        self.shop_button.pack(side=tk.LEFT)

        # Initialize video capture and recording variables
        self.video_capture = cv2.VideoCapture(0)
        self.recording = False
        self.out = None

        # Exercise tracking variables
        self.current_exercise = None
        self.counter = 0

        self.detector = detector.detector(self.video_capture, "None")

        # Update video display
        self.update_video()
    def toggle_music(self):
        self.music_enabled = not self.music_enabled
        if self.music_enabled:
            pygame.mixer.init()
            pygame.mixer.music.load('music.mp3')
            pygame.mixer.music.set_endevent(pygame.constants.USEREVENT) # Comment!
            pygame.mixer.music.play(loops=-1) # plays music indefinitely
        else:
            pygame.mixer.music.stop()

    def update_video(self):
        if not self.recording:
            ret, frame = self.video_capture.read()
            if ret:
                # Flip the frame horizontally
                frame = cv2.flip(frame, 1)
                self.frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                self.photo = ImageTk.PhotoImage(image=Image.fromarray(self.frame))
                self.video_label.config(image=self.photo)
        else:
            self.frame, pose = self.detector.update()
            if self.photo is not None:
                self.photo = ImageTk.PhotoImage(image=Image.fromarray(self.frame))
                self.video_label.config(image=self.photo)
                if pose is not None:
                    if pose == self.current_exercise:
                        self.increase_exercise(pose)
                        self.increase_counter()

        self.root.after(1, self.update_video)

    def start_recording(self):
        self.recording = True
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)

    def stop_recording(self):
        self.recording = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

    def switch_exercise(self, exercise):
        self.current_exercise = exercise
        self.exercise_label.config(text=f"Exercise: {exercise}")
        self.counter = 0
        self.detector.change_type(exercise)
        self.update_counters()
    def increase_exercise(self, pose):
        match pose:
            case "Pushups":
                self.total_pushups += 1
            case "Squats":
                self.total_squats += 1
            case "Situps":
                self.total_situps += 1
       
        self.update_counters()

            
    def update_counters(self):
        self.counter_label.config(text=f"Count: {self.counter}")
        self.pushup_counter_label.config(text=f"Total Pushups: {self.total_pushups}")
        self.squats_counter_label.config(text=f"Total Squats: {self.total_squats}")
        self.situps_counter_label.config(text=f"Total Situps: {self.total_situps}")
        self.money_counter_label.config(text=f"Money $DUCK: {self.money}")

    def increase_counter(self):
        self.counter += 1
        self.money += 1
        self.update_counters()

    
    
    def shop(self):
        root = tk.Tk()
        root.title("Shop")
        style = ttk.Style(root)
        style.theme_use("clam")
        shop_label = tk.Label(root, text="Shop")
        inventory_label = tk.Label(root, text="Inventory")

        # Create text widgets for displaying text in columns
        shop_text = tk.Label(root, height=10, width=30)
 
        inventory_text = tk.Label(root, height=10, width=30)


        # Create a single text entry widget
        entry_field = tk.Entry(root, width=30)

        # Arrange labels, text widgets, and entry widgets in the grid
        shop_label.grid(row=0, column=0, padx=10, pady=5)
        inventory_label.grid(row=0, column=1, padx=10, pady=5)
        shop_text.grid(row=1, column=0, padx=10, pady=5)
        inventory_text.grid(row=1, column=1, padx=10, pady=5)
        entry_field.grid(row=2, column=0, columnspan=2, padx=10, pady=5)

        ntext = ""
        for i in self.inventory:
            ntext +=   i + "\n"
        inventory_text.config(text=ntext)
        ntext = ""
        for i in range(len(self.shop_items)):
            if i % 2 == 0:
                ntext += str(int(i/2)) + ". " + self.shop_items[i] + " "
            else:
                ntext += self.shop_items[i] + ": $DUCK\n"
        shop_text.config(text= ntext)

        # Create a modal dialog to wait for input
        def get_input(a):
            # After input received
            input_text = entry_field.get()
            item = int(input_text) * 2
            if(self.money >= int(self.shop_items[item + 1])):
                self.money -= int(self.shop_items[item + 1])
                self.inventory.append(self.shop_items[item])
            self.update_counters()
            ntext = ""
            for i in self.inventory:
                ntext +=   i + "\n"
            inventory_text.config(text=ntext)
        entry_field.bind("<Return>", get_input)


        
        root.mainloop()
        

# Define custom style for rounded buttons
root = tk.Tk()
root.title("Video Recorder App")

style = ttk.Style(root)
style.theme_use("clam")

style.configure("My.TFrame", background="#191414", borderwidth=0, relief=tk.FLAT)
style.configure("My.TButton", background="#1DB954", foreground="white", borderwidth=0, relief=tk.FLAT, font=("Spotify", 14))
style.map("My.TButton", background=[("active", "#1ed760")])

# Custom style for the "Stop Recording" button
style.configure("MyStop.TButton", background="#FF0000", foreground="white", borderwidth=0, relief=tk.FLAT, font=("Spotify", 14))
style.map("MyStop.TButton", background=[("active", "#FF3030")])

app = VideoRecorderApp(root)
root.mainloop()
