import customtkinter as ctk
from Pawsword.control import load_vault, vault_exists
from Pawsword.ui.frames.login_f import LoginFrame
from Pawsword.ui.frames.vault_f import VaultFrame
from tkinter import PhotoImage
import os
import sys

app = ctk.CTk()

app.geometry('900x700')

app.resizable(False, False)

app.title('Pawsword')

current_dir = os.path.dirname(os.path.abspath(__file__))
if sys.platform == "win32":
    icon_path = os.path.join(current_dir, "../assets/cat-hacker.ico")
    icon_path = os.path.normpath(icon_path)
    if os.path.exists(icon_path):
        app.iconbitmap(icon_path)
else:
    icon_path = os.path.join(current_dir, "../assets/cat-hacker.png")
    icon_path = os.path.normpath(icon_path)
    if os.path.exists(icon_path):
        icon = PhotoImage(file=icon_path)
        app.iconphoto(True, icon)

app.frames = {}

def show_frame(f):
    for frame in app.frames.values():
        frame.pack_forget()
    app.frames[f].pack(fill="both", expand=True)

app.frames["login"] = LoginFrame(app,show_frame)
app.frames["vault"] = VaultFrame(app,show_frame)

show_frame("login")

if __name__ == '__main__':
    app.mainloop()