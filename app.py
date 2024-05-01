import tkinter as tk
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
                time.sleep(15)
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
    start.grid_remove()
    list_box.delete(0, "end")
    thread().start()


display = False
def toggle():
    global display
    if display :
        # btn1.grid()
        start.grid()
        toggle.grid(row=2, column=1)
        display = False
        toggle.config(text="hide")
    else:
        # btn1.grid_remove()
        start.grid_remove()
        toggle.grid(row=0,column=1, rowspan=2)
        display = True
        toggle.config(text="show")

    root.overrideredirect(display)



root = tk.Tk()
root.title("spotify lyrics")

# Set the window always on top
root.wm_attributes("-topmost", True)
# Make the window non-resizable
root.resizable(width=False, height=False)

# following line will make every bg transparent having color red
hidden_color = "black"
root.wm_attributes("-transparentcolor", hidden_color)

frame = tk.Frame(root, bd=2, relief="solid", bg=hidden_color)
frame.pack()

button_width = 12
label_width = 40

# btn1 = tk.Button(frame, text="generate token", width=button_width, command=generate_token)
start = tk.Button(frame, text="start", width=button_width, command=start)
toggle = tk.Button(frame, text="hide", width=button_width, command=toggle)

status = tk.Label(frame, width=label_width, bg=hidden_color, fg="white")
label1 = tk.Label(frame, text="label1", width=label_width, bg=hidden_color, fg="white")
label2 = tk.Label(frame, text="label2", width=label_width, bg=hidden_color, fg="white")

labels = [status, label1, label2]

# btn1.grid(row=0, column=1)
start.grid(row=1, column=1)
toggle.grid(row=2, column=1)

# status.grid(row=0, column=0)
# label1.grid(row=1, column=0, pady=5)
# label2.grid(row=2, column=0)

list_box = tk.Listbox(frame, bg="black", fg="white", width=50, height=(start.winfo_height()*3))
list_box.grid(row=1, column=0, rowspan=3)

root.mainloop()
