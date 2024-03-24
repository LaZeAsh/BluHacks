import tkinter as tk
import cv2
from PIL import Image, ImageTk
import threading

class VideoRecorderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Video Recorder App")

        self.video_label = tk.Label(self.root)
        self.video_label.pack()

        self.start_button = tk.Button(self.root, text="Start Recording", command=self.start_recording)
        self.start_button.pack()

        self.stop_button = tk.Button(self.root, text="Stop Recording", command=self.stop_recording, state=tk.DISABLED)
        self.stop_button.pack()

        self.video_capture = cv2.VideoCapture(0)
        self.recording = False
        self.out = None

        self.update_video()

    def update_video(self):
        ret, frame = self.video_capture.read()
        if ret:
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
        self.recording_thread.join()
        self.out.release()

    def record_video(self):
        fourcc = cv2.VideoWriter_fourcc(*'MJPG')
        frame_width = int(self.video_capture.get(3))
        frame_height = int(self.video_capture.get(4))
        self.out = cv2.VideoWriter("output.avi", fourcc, 20, (frame_width, frame_height))

        while self.recording:
            ret, frame = self.video_capture.read()
            if ret:
                self.out.write(frame)
            else:
                break

if __name__ == "__main__":
    root = tk.Tk()
    app = VideoRecorderApp(root)
    root.mainloop()
