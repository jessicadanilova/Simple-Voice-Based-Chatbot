import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import time
import os
import textwrap
from tkinter import Tk, Label, Button, Entry, messagebox
from tkinter.ttk import Progressbar

def record_audio(duration, sentence):
    fs = 44100
    print(f"Get ready! Recording will start in:")
    for i in range(3, 0, -1):
        print(f"{i}...")
        countdown_label.config(text=f"{i}...")
        root.update()
        time.sleep(1)

    print(f"Recording started. Please read the following sentence:")
    
    wrapped_sentence = textwrap.fill(sentence, width=50)
    sentence_label.config(text=wrapped_sentence)
    root.update()

    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype=np.int16)
    for i in range(duration):
        progress = int((i+1) / duration * 100)
        progress_label.config(text=f"Recording progress: {progress}%")
        progress_bar["value"] = progress
        root.update()
        time.sleep(1)
    
    progress_label.config(text="Recording progress: 100%")
    progress_bar["value"] = 100
    root.update()
    time.sleep(0.5)  # Just to display the progress at 100% for a moment

    while True:
        filename = filename_var.get().strip()
        if filename:
            filename = os.path.join("Recordings", f"{filename}.wav")
            if os.path.exists(filename):
                base_filename, ext = os.path.splitext(filename)
                index = 2
                while True:
                    new_filename = f"{base_filename}_{index}{ext}"
                    if not os.path.exists(new_filename):
                        filename = new_filename
                        break
                    index += 1
            break
        else:
            messagebox.showerror("Error", "Filename cannot be empty.")
            return

    fs = 44100
    wav.write(filename, fs, recording)
    print(f"Recording saved as: {filename}")
    messagebox.showinfo("Recording Saved", f"Recording saved as: {filename}")
    ask_try_again()

def ask_try_again():
    try_again = messagebox.askyesno("Try Again", "Do you want to try again?")
    if try_again:
        reset_gui()
    else:
        ask_record_another_sample()

def ask_record_another_sample():
    record_another = messagebox.askyesno("Record Another Sample", "Do you want to record another sample?")
    if record_another:
        reset_gui()
    else:
        exit()

def reset_gui():
    countdown_label.config(text="")
    sentence_label.config(text="")
    progress_label.config(text="")
    progress_bar["value"] = 0
    filename_var.set("")

def start_recording_activity():
    duration = duration_var.get()
    sentence = sentence_var.get()
    filename = filename_var.get()
    if not duration or not sentence or not filename:
        messagebox.showerror("Error", "Please enter duration, sentence, and filename.")
        return
    record_audio(int(duration), sentence)

def quit_application():
    root.destroy()

# Create the root window
root = Tk()
root.title("Audio Recorder")

# Calculate the position to center the window
window_width = 800
window_height = 600
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_position = (screen_width - window_width) // 2
y_position = (screen_height - window_height) // 2

# Set the window size and position
root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

duration_label = Label(root, text="Recording Duration (in seconds):", font=("Helvetica", 16))
duration_label.grid(row=0, column=0, sticky="e")
duration_var = Entry(root, font=("Helvetica", 16))
duration_var.grid(row=0, column=1)

sentence_label = Label(root, text="Sentence to Read:", font=("Helvetica", 16))
sentence_label.grid(row=1, column=0, sticky="e")
sentence_var = Entry(root, font=("Helvetica", 16))
sentence_var.grid(row=1, column=1)

filename_label = Label(root, text="Enter Filename:", font=("Helvetica", 16))
filename_label.grid(row=2, column=0, sticky="e")
filename_var = Entry(root, font=("Helvetica", 16))
filename_var.grid(row=2, column=1)

countdown_label = Label(root, text="", font=("Helvetica", 20))
countdown_label.grid(row=3, columnspan=2)

sentence_label = Label(root, text="", font=("Helvetica", 20))
sentence_label.grid(row=4, columnspan=2)

progress_label = Label(root, text="", font=("Helvetica", 20))
progress_label.grid(row=5, columnspan=2)

progress_bar = Progressbar(root, orient="horizontal", length=600, mode="determinate")
progress_bar.grid(row=6, columnspan=2)

record_button = Button(root, text="Start Recording", command=start_recording_activity, font=("Helvetica", 16), width=20, height=3)
record_button.grid(row=7, columnspan=2)

quit_button = Button(root, text="Quit", command=quit_application, font=("Helvetica", 16), width=20, height=3)
quit_button.grid(row=8, columnspan=2)

root.mainloop()
