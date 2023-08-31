import tkinter as tk
from tkinter import filedialog, Canvas
from datetime import datetime
import cv2
from PIL import Image, ImageTk
import threading

# Store photo paths
selected_photo_paths = []
video_name = ""
video_frame = None

def select_photos():
    global selected_photo_paths
    selected_photo_paths = list(filedialog.askopenfilenames(initialdir="/", title="Select Photos", filetypes=(("JPEG files", "*.jpg"), ("PNG files", "*.png"), ("All files", "*.*"))))
    num_selected = len(selected_photo_paths)
    selection_label.config(text=f"{num_selected} images selected", font=("Helvetica", 10, "italic"))

def combine_photos():
    global selected_photo_paths, video_name

    if not selected_photo_paths:
        print("No photos selected.")
        return

    try:
        frames_per_second = int(fps_entry.get())
    except ValueError:
        print("Invalid FPS value. Using default 24 FPS.")
        frames_per_second = 24

    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    video_name = f"output_{current_time}.mp4"

    frame_width, frame_height = 0, 0
    video_writer = None
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')

    for photo_path in selected_photo_paths:
        frame = cv2.imread(photo_path)
        if frame_width == 0 or frame_height == 0:
            frame_height, frame_width, _ = frame.shape
            video_writer = cv2.VideoWriter(video_name, fourcc, frames_per_second, (frame_width, frame_height))

        frame = cv2.resize(frame, (frame_width, frame_height))
        video_writer.write(frame)

    video_writer.release()
    print(f"Photos combined into an MP4 file: {video_name}")
    play_video()

def play_video():
    global video_name, video_frame

    cap = cv2.VideoCapture(video_name)

    def update_frame():
        ret, frame = cap.read()

        if ret:
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
            img = Image.fromarray(cv2image).resize((300, 300))
            imgtk = ImageTk.PhotoImage(image=img)
            video_frame.imgtk = imgtk
            video_frame.config(image=imgtk)
            video_frame.after(10, update_frame)

    update_frame()
    
#=============================================================================================================
#=============================================================================================================

# Create a Tkinter window
window = tk.Tk()
window.geometry("800x600")  # Set the window size to 800x600 pixels
window.attributes('-alpha', 0.93)  # Sets window to 70% opacity
window.configure(bg='#1A001A')  # Very dark magenta, almost black

# Create a frame to contain all widgets and set its background
frame = tk.Frame(window, bg='#1A001A')
frame.pack(pady=20)

# Add a title at the top
title_label = tk.Label(frame, text="stitcher", font=("Courier", 34), bg='#1A001A', fg='white')
title_label.grid(row=0, columnspan=2, pady=10)

# Add a button to select photos
select_button = tk.Button(frame, text="Select Photos", command=select_photos, bg='#333333', fg='black')
select_button.grid(row=1, columnspan=2, pady=10)

# Add a label to show number of selected images
selection_label = tk.Label(frame, text="No images selected", font=("Helvetica", 10, "italic"), bg='#1A001A', fg='white')
selection_label.grid(row=2, columnspan=2, pady=10)

# Add label and entry to get FPS
fps_label = tk.Label(frame, text="Enter FPS:", bg='#1A001A', fg='white')
fps_label.grid(row=3, column=0, pady=10, sticky='e')

fps_entry = tk.Entry(frame)
fps_entry.grid(row=3, column=1, pady=2, sticky='w')
fps_entry.insert(0, "24")  # Default FPS value

# Add a button to create video
create_button = tk.Button(frame, text="Create Video", command=combine_photos, bg='#333333', fg='black')
create_button.grid(row=4, columnspan=2, pady=10)

# Create a canvas for the video display, with softened edges
canvas = tk.Canvas(frame, bg='grey', width=300, height=300)
canvas.grid(row=5, columnspan=2, pady=10)
canvas.create_rectangle(3, 3, 297, 297, outline="#A9A9A9", width=4)

# Use this canvas for video_frame
video_frame = tk.Label(canvas)
video_frame.place(x=3, y=3)

# Run the Tkinter event loop
window.mainloop()
