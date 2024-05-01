from dotenv import load_dotenv
import os
import requests
import secrets
import tkinter as tk
from tkinter import messagebox
import webbrowser
from urllib.parse import urlparse, parse_qs
import json

load_dotenv()
auth_url = "https://accounts.spotify.com/authorize"
token_url = "https://accounts.spotify.com/api/token"


def generate_token():

    def open_link(event):
        webbrowser.open(response.url)

    def handle_submit():
        if(entry.get() != ""):
            parsed_url = urlparse(entry.get())
            authorization_code = parse_qs(parsed_url.query)['code'][0]
            
            token_response = requests.post(token_url, data={
                        "grant_type": "authorization_code",
                        "code": authorization_code,
                        "redirect_uri": os.getenv("REDIRECT_URI"),
                        "client_id": os.getenv("CLIENT_ID"),
                        "client_secret": os.getenv("CLIENT_SECRET")
                    })

            if(token_response.json().get("access_token")):
                with open(f"auth_token.json", "w") as f:
                    json.dump(token_response.json(), f)
                    submit.grid_forget()
                    status.config(text="token generated successfully", fg="blue")
                    messagebox.showinfo("success", "Token successfully generated!")
                    window.destroy()
                # Use access token to make authorized API requests
            else:
                messagebox.showinfo(token_response.json().get("error"), token_response.json().get("error_description"))


        else:
            status.config(text="please paste redirected url")


    response = requests.get(auth_url, params={
        "response_type": "code",
        "client_id": os.getenv("CLIENT_ID"),
        "redirect_uri": os.getenv("REDIRECT_URI"),
        "scope": os.getenv("SCOPE"),
        "state": secrets.token_hex(16) #generate random hexadecimal string of length 16
        })

    window = tk.Tk()
    window.title("token generator")

    tk.Label(window, text="1. click on link given below to login and give permition.").pack(anchor="w")

    link_label = tk.Label(window, text="Click here to visit auth page", fg="blue", cursor="hand2")
    link_label.pack()

    tk.Label(window, text="2. copy the redirected pages url").pack(anchor="w")
    tk.Label(window, text="3. paste the copied url in textbox given below").pack(anchor="w")

    frame = tk.Frame(window)
    entry = tk.Entry(frame)
    entry.grid(row=0, column=0)
    submit = tk.Button(frame, text="submit", command=handle_submit)
    submit.grid(row=0, column=1)
    frame.pack()

    status = tk.Label(window, text="click 'submit' to generate token", fg="red")
    status.pack()

    # Bind the label to open the link in a web browser when clicked
    link_label.bind("<Button-1>", open_link)
    window.mainloop()

# generate_token()