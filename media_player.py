import tkinter as tk
from tkinter import filedialog, messagebox
from pygame import mixer
import time

class MediaPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("Media Player")
        mixer.init()
        self.create_widgets()
        self.file_path = ""
        self.volume = 0.5
        self.paused = False
        self.music_length = 0

    def create_widgets(self):
        # Creating control frame
        control_frame = tk.Frame(self.root)
        control_frame.pack(pady=10)
        # Creating open button for opening audio file
        self.SelectFile = tk.Button(control_frame, text="Open", command=self.select_file, width=8)
        self.SelectFile.pack(side=tk.LEFT)
        # Creating play button to play the audio file from start
        self.Play = tk.Button(control_frame, text="Play", command=self.play_file, state=tk.DISABLED, width=8)
        self.Play.pack(side=tk.LEFT)
        # Creating pause button
        self.Pause = tk.Button(control_frame, text="Pause", command=self.pause_file, state=tk.DISABLED, width=8)
        self.Pause.pack(side=tk.LEFT)
        # Creating stop button to end the audio file
        self.Stop = tk.Button(control_frame, text="Stop", command=self.stop_file, state=tk.DISABLED, width=8)
        self.Stop.pack(side=tk.LEFT)
        # Creating volume increase button
        self.VolumeUp = tk.Button(control_frame, text="+", command=self.increase_volume, width=4)
        self.VolumeUp.pack(side=tk.LEFT)
        # Creating volume decrease button
        self.VolumeDown = tk.Button(control_frame, text="-", command=self.decrease_volume, width=4)
        self.VolumeDown.pack(side=tk.LEFT)
        # Deafault message on screen when no file is chosen
        self.label_file = tk.Label(self.root, text="No file selected", font=("Arial", 14, "bold"), bg="black",
                                   fg="white", pady=5, padx=10)
        self.label_file.pack(fill=tk.X)
        # Creating label for displaying song name
        self.label_song_name = tk.Label(self.root, text="", font=("Arial", 16), bg="black", fg="white", pady=10)
        self.label_song_name.pack()

        # Creating music slider
        self.music_slider = tk.Scale(self.root, from_=0, to=100, orient=tk.HORIZONTAL, length=200, showvalue=0,
                                 command=self.set_music_position)
        self.music_slider.pack()

        # Creating label for displaying playback time
        self.label_playback_time = tk.Label(self.root, text="00:00 / 00:00", font=("Arial", 12), bg="black", fg="white")
        self.label_playback_time.pack()

        # Creating status label
        self.status_label = tk.Label(self.root, text="", font=("Arial", 12), bg="black", fg="white")
        self.status_label.pack()

    def select_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Audio Files", ("*.mp3", "*.wav", "*.ogg"))])
        if file_path:
            self.file_path = file_path
            self.label_file.pack_forget()
            self.label_song_name.config(text="")
            self.Play.config(state=tk.NORMAL)
            self.update_status("File selected")
            self.update_status("Playing")
            self.play_media()

    def play_file(self):
        self.play_media()
        self.update_status("Playing")

    def pause_file(self):
        if not self.paused:
            mixer.music.pause()
            self.update_status("Paused")
        else:
            mixer.music.unpause()
            self.update_status("Resumed")
        self.paused = not self.paused
        self.update_playback_time()

    def stop_file(self):
        mixer.music.stop()
        self.Pause.config(state=tk.DISABLED)
        self.Stop.config(state=tk.DISABLED)
        self.update_status("Stopped")
        self.update_playback_time()

    def increase_volume(self):
        new_volume = self.volume + 0.1
        if new_volume <= 1:
            self.volume = new_volume
            mixer.music.set_volume(self.volume)
            self.update_status("Volume increased")

    def decrease_volume(self):
        new_volume = self.volume - 0.1
        if new_volume >= 0:
            self.volume = new_volume
            mixer.music.set_volume(self.volume)
            self.update_status("Volume decreased")

    def set_volume(self, volume):
        self.volume = float(volume)
        mixer.music.set_volume(self.volume)

    def play_media(self):
        try:
            mixer.music.load(self.file_path)
            self.music_length = mixer.Sound(self.file_path).get_length()  # Get the length of the audio file
            self.music_slider.config(from_=0, to=self.music_length)  # Set the range of the music slider
            mixer.music.play()
            self.Pause.config(state=tk.NORMAL)
            self.Stop.config(state=tk.NORMAL)
            song_name = self.file_path.split("/")[-1]
            self.label_song_name.config(text=song_name)
            self.update_playback_time()
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.stop_file()
            self.update_status("Error: " + str(e))

    def set_music_position(self, position):
        position_seconds = float(position)
        self.music_slider.set(position_seconds)
        mixer.music.pause()
        mixer.music.set_pos(position_seconds)
        mixer.music.unpause()
        self.update_playback_time()


    def update_playback_time(self):
        if mixer.music.get_busy() and not self.paused:
            current_position = mixer.music.get_pos() / 1000  # Get current position in seconds
            current_time = time.strftime('%M:%S', time.gmtime(current_position))  # Format current position
            total_time = time.strftime('%M:%S', time.gmtime(self.music_length))  # Format total audio length
            playback_time = f"{current_time} / {total_time}"
            self.label_playback_time.config(text=playback_time)
            self.music_slider.set(current_position)
            self.root.after(1000, self.update_playback_time)

    def update_status(self, status):
        self.status_label.config(text="Status: " + status)


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("400x200")
    root.config(bg="black")
    media_player = MediaPlayer(root)
    root.mainloop()
