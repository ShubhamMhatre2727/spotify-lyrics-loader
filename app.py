import tkinter as tk
from tkinter import colorchooser
import json
import time
import threading
import requests
from generate_auth_token import generate_token
from get_current_track import get_track

class thread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    
    def run(self):
        current_track = get_track()
        if(current_track):
            if current_track['currently_playing_type'] == "ad":
                list_box.insert(0, "ad playing")
                # print("ad playing")
                time.sleep(30)
                list_box.delete(0, "end")
                self.run()

            else:
                root.title(current_track["name"])
                results = requests.get(f"https://lrclib.net/api/search?track_name={current_track['name']}&artist_name={current_track['artist']}").json()

                synced_lyrics = results[0]['syncedLyrics']
                if(synced_lyrics != None):
                    self.generate_lyrics(synced_lyrics, current_track)
                else:
                    status.config(text="lyrics not found")
        else:
            start.config(state="normal")
    
    def generate_lyrics(self, synced_lyrics, current_track):
        try:
            list = synced_lyrics.split("\n")
            i = 0
            prev = float(current_track["progress"])
            
            while (float(list[i][1:3]) * 60 + float(list[i][4:6]) <= prev):
                i += 1 
            
            self.display_lyrics(i, list, prev, current_track)
        except (IndexError):
            list_box.delete(0, "end")
            self.run()

    def display_lyrics(self, i, list, prev, current_track):
        if(i<len(list)):
            # print(list[i][11:])
            list_box.insert(i, list[i][11:])
            list_box.see("end")
            curr = float(list[i][1:3]) * 60 + float(list[i][4:6])
            sleep_time = (curr - prev)
            prev = curr
            i+=1
            time.sleep(sleep_time)
            self.display_lyrics(i, list, prev, current_track)
        time.sleep(current_track['duration']-prev)
        list_box.delete(0, "end")
        self.run()

        




def start():
    start.config(state="disabled")
    list_box.delete(0, "end")
    thread().start()


display = False
def toggle():
    global display
    if display :
        start.grid()
        close.grid()
        toggle.grid(row=1, column=1)
        display = False
        toggle.config(text="hide", width=button_width)
        color.config(width=button_width)
    else:
        start.grid_remove()
        close.grid_remove()
        toggle.grid(row=0,column=1)
        display = True
        toggle.config(text="X", width=5)
        color.config(width=5)

    root.overrideredirect(display)


def change_color():
    if list_box.cget("foreground") == "white":
        list_box.config(fg="black")
        color.config(text="⚪")
    else: 
        list_box.config(fg="white")
        color.config(text="⚫")

root = tk.Tk()
root.title("spotify lyrics")
# Set the window always on top
root.wm_attributes("-topmost", True)
# Make the window non-resizable
root.resizable(width=False, height=False)

# following line will make every bg transparent having color red
hidden_color = "gray"
root.wm_attributes("-transparentcolor", hidden_color)

frame = tk.Frame(root, bg=hidden_color)
frame.pack()

button_width = 12
start = tk.Button(frame, text="start", width=button_width, command=start)
toggle = tk.Button(frame, text="hide", width=button_width, command=toggle)
close = tk.Button(frame, text="close", width=button_width, command=lambda:root.destroy())
color = tk.Button(frame, text="⚫", width=button_width, command=change_color)

list_box = tk.Listbox(frame, bg=hidden_color,bd=0, font=("", 12, "bold"), justify="right" ,highlightthickness=0 , fg="white", width=50, height=(start.winfo_height()*3))
list_box.insert(0, "sample text")
start.grid(row=0, column=1)
toggle.grid(row=1, column=1)
close.grid(row=2, column=1)
color.grid(row=3, column=1)

list_box.grid(row=0, column=0, rowspan=4, padx=10)

root.mainloop()