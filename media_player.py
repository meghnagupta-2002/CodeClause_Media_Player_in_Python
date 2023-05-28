import tkinter as tk
from tkinter import filedialog, messagebox
from pygame import mixer

class MediaPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("Media Player")
        mixer.init()
        self.create_widgets()
        self.file_path = ""
        self.volume = 0.5
        self.paused = False

    def create_widgets(self):
        #Creating control frame
        control_frame = tk.Frame(self.root)
        control_frame.pack(pady=10)
        #Creating open button for opening audio file
        self.SelectFile = tk.Button(control_frame, text="Open", command=self.select_file, width=8)
        self.SelectFile.pack(side=tk.LEFT)
        #Creating play button to play the audio file from start
        self.Play = tk.Button(control_frame, text="Play", command=self.play_file, state=tk.DISABLED, width=8)
        self.Play.pack(side=tk.LEFT)
        #Creating pause button 
        self.Pause = tk.Button(control_frame, text="Pause", command=self.pause_file, state=tk.DISABLED, width=8)
        self.Pause.pack(side=tk.LEFT)
        #Creating stop button to end the audio file
        self.Stop = tk.Button(control_frame, text="Stop", command=self.stop_file, state=tk.DISABLED, width=8)
        self.Stop.pack(side=tk.LEFT)
        #Creating volume increase button
        self.VolumeUp = tk.Button(control_frame, text="+", command=lambda: self.change_volume(0.1), width=4)
        self.VolumeUp.pack(side=tk.LEFT)
        #Creating volume decrease button
        self.VolumeDown = tk.Button(control_frame, text="-", command=lambda: self.change_volume(-0.1), width=4)
        self.VolumeDown.pack(side=tk.LEFT)
        #deafault message on screen when no file is chosen
        self.label_file = tk.Label(self.root, text="No file selected", font=("Arial", 14,"bold"), bg="black", fg="white", pady=5, padx=10)
        self.label_file.pack(fill=tk.X)
        #Creating label for displaying song name
        self.label_song_name = tk.Label(self.root, text="", font=("Arial", 16), bg="black", fg="white", pady=10)
        self.label_song_name.pack()

    def select_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Audio Files", ("*.mp3", "*.wav", "*.ogg"))])
        if file_path:
            self.file_path = file_path
            #self.label_file.config(text=self.file_path) ...shows the path of file selected
            self.label_song_name.config(text="")
            #Enable the play button
            self.Play.config(state=tk.NORMAL)
            #Auto play the selected file
            self.play_media()
     
    def play_file(self):                                        #Triggered when user clicks play button
        self.play_media()                                       #Initiate playback by calling play_media fucntion
    
    def pause_file(self):                                       #Triggered when user clicks pause button
        if not self.paused:
            mixer.music.pause()                                 #pause audio
        else:
            mixer.music.unpause()                               #resume audio
        self.paused = not self.paused

    def stop_file(self):                                        #Triggered when user clicks stop button
        mixer.music.stop()                                      #stop audio
        self.Pause.config(state=tk.DISABLED)                    #disable pause button
        self.Stop.config(state=tk.DISABLED)                     #disable stop button

    def change_volume(self, value):                             #Triggered when user clicks '+'/'-' button
        new_volume = self.volume + value
        if 0 <= new_volume <= 1:
            self.volume = new_volume
            mixer.music.set_volume(self.volume)

    def play_media(self):
        try:
            mixer.music.load(self.file_path)                    #load selected file
            mixer.music.play()                                  #start playing selected file
            self.Pause.config(state=tk.NORMAL)                  #enable pause button
            self.Stop.config(state=tk.NORMAL)                   #enable stop button
            song_name = self.file_path.split("/")[-1]
            self.label_song_name.config(text=song_name)         #display song name
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.stop_file()


if __name__ == "__main__":
    root = tk.Tk()                                              #Creating root window
    #Setting dimensiond and background color
    root.geometry("400x200")
    root.config(bg="black")
    media_player = MediaPlayer(root)
    root.mainloop()
